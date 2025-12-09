from celery.schedules import crontab

imports = (
    "workers.tasks.asr",
    "workers.tasks.enrich",
    "workers.tasks.summarize",
    "workers.tasks.analytics",
    "workers.tasks.persist",
    "workers.tasks.nightly_dedup",
)

# Route queues
task_routes = {
    "workers.tasks.asr.*": {"queue": "asr"},
    "workers.tasks.diarize.*": {"queue": "diarize"},
    "workers.tasks.enrich.*": {"queue": "enrich"},
    "workers.tasks.summarize.*": {"queue": "summarize"},
    "workers.tasks.analytics.*": {"queue": "analytics"},
    "workers.tasks.persist.*": {"queue": "persist"},
    "workers.tasks.webhooks.*": {"queue": "notify"},
}

# Beat schedule: nightly dedup 4:00 AM local
beat_schedule = {
    "nightly-dedup": {
        "task": "workers.tasks.nightly_dedup.run",
        "schedule": crontab(minute=0, hour=4),
    }
}
