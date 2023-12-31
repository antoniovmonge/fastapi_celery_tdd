import os
import pathlib
from functools import lru_cache

from kombu import Queue

def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "default"}

class BaseConfig:
    """
    We are not using pydantic BaseSettings here because it might cause\
    Celery to raise [ERROR/MainProcess] pidbox command error:\
    KeyError('__signature__') error when we launch Flower.
    """

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
    DATABASE_CONNECT_DICT: dict = (
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )

    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )

    WS_MESSAGE_QUEUE: str = os.environ.get(
        "WS_MESSAGE_QUEUE", "redis://127.0.0.1:6379/0"
    )

    CELERY_TASK_ALWAYS_EAGER: bool = False

    CELERY_BEAT_SCHEDULE: dict = {
        # "task-schedule-work": {
        #     "task": "task_schedule_work",
        #     "schedule": 5.0,  # five seconds
        # },
    }

    CELERY_TASK_DEFAULT_QUEUE: str = "default"

    # Force all queues to be explicitly listed in `CELERY_TASK_QUEUES` to help prevent typos
    CELERY_TASK_CREATE_MISSING_QUEUES: bool = False

    CELERY_TASK_QUEUES: list = (
        # need to define default queue here or exception would be raised
        Queue("default"),

        Queue("high_priority"),
        Queue("low_priority"),
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    """
    Override some settings for development.
    """

    # CELERY_TASK_ALWAYS_EAGER: bool = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
