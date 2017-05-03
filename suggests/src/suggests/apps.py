from datetime import datetime

from django.apps import AppConfig
from django.conf import settings


class SuggestsConfig(AppConfig):

    name = 'suggests'

    def ready(self):

        import django_rq
        from suggests import tasks

        scheduler = django_rq.get_scheduler(settings.APP_NAME)

        # Cancel all jobs already started
        for job in scheduler.get_jobs():
            scheduler.cancel(job)

        # SCHEDULER CONFIGURATION

        # - Updating suggests tree
        scheduler.schedule(
            scheduled_time=datetime.utcnow(),
            func=tasks.update_suggests,
            interval=settings.SUGGESTS_UPDATE_INTERVAL,
            repeat=None,
            result_ttl=settings.SUGGESTS_UPDATE_INTERVAL + 100
        )
