import logging
import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from movie_tickets.models import Movie


logger = logging.getLogger(__name__)

@transaction.atomic
class Command(BaseCommand):
    help = 'Add a movie to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--commit',
            '-c',
            action='store_true',
            dest='commit',
            default=False,
            help=("Save the movie to the database."),
        )
        json_default_path = 'movie_tickets/management/conf/movie_data.json'
        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        movie_default_path = os.path.join(BASE_DIR, json_default_path)

        parser.add_argument(
            '--file',
            '-f',
            dest='file',
            default=movie_default_path,
            help="Movie list file.",
        )
    def handle(self, *args, **options):
        sid = transaction.savepoint()
        # load json file from conf/movie_data.json
        # iterate over the movies and add them to the database
        with open(options['file']) as f:
            movies = json.load(f)
        for movie in movies:
            title = movie['title']
            genre = movie['description']
            logger.info(f'Adding movie {title} to the database')
            Movie.objects.create(title=title, genre=genre)
            logger.info('Movie added successfully')

        if options['commit']:
            logger.info(self.style.SUCCESS("Successful commit"))
            transaction.savepoint_commit(sid)
        else:
            logger.info(self.style.WARNING("Dry run, rolling back"))
            transaction.savepoint_rollback(sid)
