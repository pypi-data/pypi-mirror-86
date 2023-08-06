# coding=utf-8

from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__)


def init_app(app):
    """Initalizes the application with the extension.

    :param app: The Flask application object.
    """
    celery.conf.broker_url = app.config['BROKER_URL']
    celery.conf.update(app.config)
    celery.config_from_object(CeleryBeatConfig())  # Load Celery Beat instance config

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


class CeleryBeatConfig(object):
    def __init__(self):
        """CeleryBeatConfig constructor"""
        self.CELERY_TASK_SERIALIZER = 'json'
        self.CELERY_RESULT_SERIALIZER = 'json'
        self.CELERY_ACCEPT_CONTENT = ['json']
        self.CELERY_IMPORTS = ('mercury.services.tasks.notification', )
        self.CELERY_TIMEZONE = 'UTC'
        self.CELERY_TASK_RESULT_EXPIRES = 30

        self.CELERYBEAT_SCHEDULE = {
            'route_notifications': {
                'task': 'mercury.services.tasks.notification.route_notifications',
                'schedule': crontab(minute='*'),  # Every minute
            }
        }
