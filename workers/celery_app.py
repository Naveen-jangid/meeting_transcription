from celery import Celery
import os

celery = Celery(
    "fire_meeting_engine",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)
celery.autodiscover_tasks(["workers.tasks"])
