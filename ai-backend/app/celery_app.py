from __future__ import annotations
from celery import Celery
from celery.signals import worker_process_init

from app.config import settings


@worker_process_init.connect
def init_worker(**kwargs):
    from app.services.engine_registry import initialize_backends
    initialize_backends()

celery_app = Celery(
    "timbre_share",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.tts_tasks", "app.tasks.clone_tasks", "app.tasks.dub_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
