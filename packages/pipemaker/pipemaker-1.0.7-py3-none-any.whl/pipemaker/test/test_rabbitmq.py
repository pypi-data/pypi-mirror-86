"""
internal python queues seems to be just as good as rabbitmq
however the code and tests for rabbitmq are working
"""

from .test_pipeline import run_async


def test_async(tmp_path):
    run_async("rabbitmq", tmp_path)
