from django.core.management.base import BaseCommand

from qua.api import tasks


class Command(BaseCommand):
    help = 'Reindex whole search database'

    def handle(self, *args, **options):

        tasks.reindex_questions.delay()

        self.stdout.write(self.style.SUCCESS('Task added to queue'))
