import logging
from datetime import datetime

import pandas as pd
import psutil

from .. import Eventq, Taskq, Workerq
from ..filesystem import Filepath

log = logging.getLogger(__name__)


class Scheduler(Taskq):
    """ taskq consumer. Handles events that update the database of tasks
    """

    # dict(url=task) of running tasks including waiting, running, completed, failed
    tasks = dict()

    def start(self, workers):
        super().start()
        self.workers = workers
        indexes = [int(w.p.name.split("_")[-1]) for w in self.workers]
        self.worker_name = self.workers[0].p.name.split("_")[0]
        self.worker_index = max(indexes) + 1

    # event handlers ####################################################

    def onRun(self, body):
        """ new tasks arrive here as dict(url=task) including upstream tasks """
        for k, v in body["tasks"].items():
            # if already scheduled then just add in the new downstream task
            current = self.tasks.get(k)
            if current:
                # finished tasks can be replaced and rerun
                if current.status in [
                    "completed",
                    "failed",
                    "failed_upstream",
                ]:
                    self.tasks.pop(k)
                # unfinished tasks can have additional downstream tasks added
                else:
                    current.downstream = current.downstream | (v.downstream)
                    continue
            v.status = "waiting"
            self.tasks[k] = v
            if not v.upstream:
                v.status = "ready"
        self.submit()

    def onRunning(self, body):
        """ finished loading data and started processing """
        task = self.tasks[body["url"]]
        task.status = "running"

    def onProgress(self, body):
        """ handles event fired by task to show progress """
        task = self.tasks[body["url"]]
        task.progress = int(body["progress"])

    def onComplete(self, body):
        """ task has completed and all output has been written """
        # update the task on data and release any downstream
        task = self.tasks[body["url"]]
        task.status = "completed"
        task.finished = body["time"]
        task.progress = 100
        task.details = ""

        # run any tasks that can now run
        for d in task.downstream:
            dtask = self.tasks[d]
            dtask.upstream.remove(task.url)
            if not dtask.upstream:
                dtask.status = "ready"
        task.downstream = set()

        # notify complete if there are consumers already but don't wait.
        Eventq().put(task.url, ch=self.chP)
        self.submit()

    def onError(self, body):
        task = self.tasks[body["url"]]
        task.status = "failed"
        task.details = str(body["exception"])

        def fail_downstream(task):
            """ recursively fail all downstream tasks """
            for d in task.downstream:
                dtask = self.tasks[d]
                dtask.status = "failed_upstream"
                dtask.details = str(task)
                fail_downstream(dtask)

        fail_downstream(task)
        self.submit()
        Eventq().put(task.url, ch=self.chP)

    def onLoading(self, body):
        """ task has been received by a workertask and is loading the data before processing """
        task = self.tasks[body["url"]]
        task.status = "loading"
        task.pid = body["pid"]
        task.process = body["process"]
        task.started = body["time"]
        task.finished = None

    def onSaving(self, body):
        """ task has finished and output is being saved """
        task = self.tasks[body["url"]]
        task.status = "saving"

    def onSetPriority(self, body):
        """ set priority for task """
        task = self.get_task(body["url"])
        task.priority = body["priority"]
        for upstream in task.upstream:
            self.tasks[upstream].priority = task.priority

    def onDelete(self, body):
        """ delete task """
        task = self.tasks.get(body["url"])
        if not task:
            return

        # remove upstream links first to prevent these triggering execution
        for u_url in task.upstream:
            self.tasks[u_url].downstream.remove(url)

        def delete_downstream(task):
            """recursively delete downstream tasks """
            for d_url in task.downstream.copy():
                delete_downstream(self.tasks[d_url])
            del self.tasks[task.url]
            log.info(f"deleted {task.url}")

        for d_url in task.downstream.copy():
            delete_downstream(self.tasks[d_url])

        # terminate process if task is running and replace worker
        if task.pid and task.status in ["loading", "running", "saving"]:
            log.info(f"terminating worker for {task.url} on {task.pid} {task.process}")
            p = psutil.Process(task.pid)
            p.kill()
            self.workers.remove(p)

            # add replacement
            w = Workerq()
            w.start(f"{self.worker_name}_{self.worker_index}")
            self.workers.append(w)
            self.worker_index += 1

        # remove task
        del self.tasks[task.url]

    def onView(self, body):
        """ puts response on eventq with dict including workers and tasks
        
        better to call view directly but this exposes data to other machines. 
        """
        Eventq().put(
            "viewkey",
            body=dict(workers=[w.p.name for w in self.workers], tasks=self.view()),
            ch=self.chP,
        )

    # internal methods #################################################################################

    def submit(self):
        """ submit to workerq top tasks that are ready """
        df = self.view()
        if len(df) == 0:
            return
        n = len(self.workers) - len(
            df[df.status.isin(["workerq", "loading", "running", "saving"])]
        )
        for task in (
            df[df.status == "ready"].sort_values("priority", ascending=False).url[:n]
        ):
            self.tasks[task].status = "workerq"
            self.workerqP.put(self.tasks[task].workertask)

    def view(self):
        """ get tasks and format as dataframe
        :return: dataframe of tasks
        """
        if len(self.tasks) == 0:
            return None

        # format tasks
        df = pd.DataFrame.from_dict([t.__dict__ for t in self.tasks.values()])
        cols = [
            "url",
            "name",
            "status",
            "priority",
            "pid",
            "process",
            "started",
            "finished",
            "elapsed",
            "remaining",
            "progress",
            "details",
        ]
        for col in set(cols) - set(df.columns):
            df[col] = None

        df.started = pd.to_datetime(df.started, errors="coerce")
        df.finished = pd.to_datetime(df.finished, errors="coerce")

        # calculated columns
        started = df.started.fillna(datetime.now())
        finished = df.finished.fillna(datetime.now())
        df["elapsed"] = (finished - started).dt.total_seconds() // 60
        df["remaining"] = df.elapsed / df.progress * 100 - df.elapsed
        if "upstream" in df.columns:
            # for waiting tasks set details=upstream
            df.loc[df.status == "waiting", "details"] = df.upstream.apply(
                lambda upstream: ",".join([str(self.tasks[url]) for url in upstream])
            )

        # not running
        df.loc[df.started.isnull(), "elapsed"] = None
        df.loc[df.started.isnull() | df.finished.notnull(), "remaining"] = None

        # formatting
        df.started = df.started[df.started.notnull()].dt.strftime("%H:%M")
        df.finished = df.finished[df.finished.notnull()].dt.strftime("%H:%M")
        df.elapsed = df.elapsed[df.elapsed.notnull()].astype(int).apply(str)
        df.remaining = df.remaining[df.remaining.notnull()].astype(int).apply(str)
        df = df[cols].fillna("").sort_values("started", ascending=False)
        return df
