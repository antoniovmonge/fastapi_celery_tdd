from celery import current_app as current_celery_app

from project.config import settings


def create_celery():
    """
    Factory function that configures and then returns a Celery app instance.
    """

    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app
