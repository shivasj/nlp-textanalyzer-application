import asyncio
import functools
import os
import traceback

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

def extract_environment_variable(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        raise RuntimeError(f"The {name} environment variable is missing.")


REDIS_URL = extract_environment_variable("REDIS_URL")

# Setup the celery worker
worker = Celery('worker', broker=REDIS_URL)

# Tasks
information_gatherer_task_running = False

@worker.task
def information_gatherer_task():
    try:
        print("Running information_gatherer_task...")
        #print(information_gatherer_task_running)


        # if information_gatherer_task_running == True:
        #     print("information_gatherer_task already running...")
        #
        # information_gatherer_task_running = True
        #
        #
        # information_gatherer_task_running = False
    except Exception as exc:
        print(str(exc))
        information_gatherer_task_running = False

# Setup the schedules
worker.conf.beat_schedule = {
    "information_gatherer_task": {
        "task": "worker.service.information_gatherer_task",
        "schedule": 30.0
    }
}