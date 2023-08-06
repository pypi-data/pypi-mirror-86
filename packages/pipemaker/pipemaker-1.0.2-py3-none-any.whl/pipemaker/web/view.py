#!python
import logging
from threading import Thread
from traceback import format_exc

import flask
import requests

log = logging.getLogger(__name__)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

app = flask.Flask(__name__)
server = None


@app.route("/shutdown")
def shutdown():
    """ shutdown flask from inside a request """
    func = flask.request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down"


@app.route("/")
def status():
    """ render html page with tables showing queues, task summary, tasks """
    try:
        # avoid circular. controller needs to start web view.
        from ..master import c

        scheduler = c.scheduler

        tables = []
        titles = []

        # workers table
        if scheduler:
            titles.append("Workers")
            workers = ", ".join([w.p.name for w in scheduler.workers])
            tables.append(f"{len(scheduler.workers)} workers: {workers}")

        # tasks
        try:
            df = scheduler.view()
        except:
            df = None

        # no tasks
        if df is None:
            titles.append("Tasks")
            tables.append("No tasks found")
        else:
            # task summary
            summary = df.groupby("status")[["url"]].count().T
            summary.columns.name = None
            status = [
                "waiting",
                "ready",
                "workerq",
                "loading",
                "running",
                "saving",
                "completed",
                "failed",
                "failed_upstream",
                "total",
            ]

            for col in set(status) - set(summary.columns):
                summary[col] = 0
            summary = summary.fillna(0)
            summary["total"] = summary.sum(axis=1)
            tables.append(summary[status].to_html(index=False, table_id="summary"))
            titles.append("Task count by status")

            # task list
            df.progress = df.loc[df.progress != ""].progress.apply(
                lambda x: str(int(x)) + "%"
            )
            df.progress = df.progress.fillna("")
            tables.append(df.to_html(table_id="task"))
            titles.append("Task list")
    except:
        log.exception("")
        titles.append("Error in server view")
        tables.append(format_exc().replace("\n", "<br>").replace(" ", "&nbsp"))

    return flask.render_template("view.html", tables=tables, titles=titles)


# control tasks  #########################################################################


def start():
    """ start flask in thread """

    global server

    def target():
        """ start flask thread """
        try:
            # reduce verbosity
            import click

            def secho(*args, **kwargs):
                pass

            def echo(*args, **kwargs):
                pass

            click.echo = echo
            click.secho = secho

            app.run(debug=False)
        except:
            log.exception("error starting flask")

    if server:
        log.debug("flask server already running")
        return
    log.debug("starting web server")
    server = Thread(target=target, daemon=True, name=__name__)
    server.start()


def stop():
    """ close flask server """
    global server

    def target():
        """ close server via shutdown request """
        try:
            r = requests.get("http://localhost:5000/shutdown")
            r.raise_for_status()
        except:
            log.warning("web server not running")

    log.debug("stopping web server")
    t = Thread(target=target, daemon=True, name=f"shutdown {__name__}")
    t.start()


def restart():
    """ restart server """
    stop()
    start()


if __name__ == "__main__":
    """ for testing. normally run in background thread """
    app.run(debug=True)
