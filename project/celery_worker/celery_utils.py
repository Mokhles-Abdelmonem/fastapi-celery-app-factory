from celery import current_app as current_celery_app

from project.config.settings import settings


def celery_app():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app