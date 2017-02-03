from django.core.management.base import BaseCommand

from qua.api import tasks


class Command(BaseCommand):
    help = 'Search index admin utility'

    def add_arguments(self, parser):

        parser.add_argument('--reindex',
            action='store_true', help='Reindex whole search index'
        )
        parser.add_argument('--link', type=str, help='Index specific link')

    def handle(self, *args, **options):

        if options['reindex']:
            tasks.reindex_questions.delay()
            self.stdout.write(self.style.SUCCESS('Task added to queue'))
        elif 'link' in options:
            tasks.index_external.delay(options['link'])
            self.stdout.write(
                self.style.SUCCESS('<%s> added to index queue' % options['link'])
            )
