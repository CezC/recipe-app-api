# minimum code to create stub for our commands
# if we run this command from djago it will probablhy run becasuse it has right structure
# with pass


"""
Django scommand to wait for the database to be available.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        pass
