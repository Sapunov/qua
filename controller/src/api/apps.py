from django.apps import AppConfig
from django.conf import settings
from django.utils import timezone


class ApiConfig(AppConfig):

    name = 'api'

    def ready(self):
        '''When application ready'''

        from api import tasks
        import django_rq

        scheduler = django_rq.get_scheduler(settings.APP_NAME)

        # Cancel all jobs already started
        for job in scheduler.get_jobs():
            scheduler.cancel(job)

        # SCHEDULER TASKS

        # 1. Update every external resource
        scheduler.schedule(
            scheduled_time=timezone.now(),
            func=tasks.update_external_resources,
            interval=settings.SCHEDULER_UPDATE_RESOURCES_INTERVAL,
            repeat=None,
            result_ttl=settings.SCHEDULER_UPDATE_RESOURCES_INTERVAL + 100
        )
