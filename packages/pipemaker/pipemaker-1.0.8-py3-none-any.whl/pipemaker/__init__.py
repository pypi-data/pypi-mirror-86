""" imports required by both master and worker
i.e. config, creds, queues
"""

import logging
import os

from . import utils

log = logging.getLogger()
log.debug(f"importing {__name__}")

# load from current, home, sys.prefix/etc, sitepackages
CONFIG = utils.load_config(".pipemaker/config.yaml")
CREDS = utils.load_config(".pipemaker/creds.yaml")

if CONFIG.qtype == "python":
    from .qpython.loghandler import SharedQueueHandler, FileHandler
    from .qpython.workerq import Workerq, WorkerqP
    from .qpython.eventq import Eventq, Eventq
    from .qpython.taskq import Taskq, TaskqP
else:
    from .qrabbit.loghandler import SharedQueueHandler, FileHandler
    from .qrabbit.workerq import Workerq, WorkerqP
    from .qrabbit.eventq import Eventq, Eventq
    from .qrabbit.taskq import Taskq, TaskqP

    # docker requires different creds
    if CONFIG.qtype == "rabbitmq" and "DOCKER" in os.environ:
        CONFIG.qtype = "docker"

    # for testing using gitlab ci (add these keys to gitlab)
    if CONFIG.qtype == "cloudamqp" and "cloudamqp_user" in os.environ:
        CREDS.cloudamqp.host = os.environ["cloudamqp_host"]
        CREDS.cloudamqp.user = os.environ["cloudamqp_user"]
        CREDS.cloudamqp.password = os.environ["cloudamqp_password"]
        CREDS.cloudamqp.vhost = os.environ["cloudamqp_vhost"]
