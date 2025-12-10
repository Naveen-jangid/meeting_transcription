from workers.celery_app import celery


@celery.task(name="workers.tasks.nightly_dedup.run")
def run():
    # 1) enumerate orgs -> 2) build temp corpus -> 3) compute similarity -> 4) write report -> 5) wipe temp
    # Use SBERT for embeddings; cosine > 0.9 => candidate duplicate
    return {"ok": True}
