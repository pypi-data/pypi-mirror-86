import os
import sys
from subprocess import Popen, PIPE
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ...dbconnect.base import get_connector


class StorageError(Exception):
    pass

class Command(BaseCommand):
    """
    docstring
    """
    def add_arguments(self,parser):
        #parser.add_argument('-d', '--database', action="store_true", help='to dump default primary database')
        parser.add_argument('-s', '--servername', help='servername')

    def handle(self, *args, **options):
        self.servername = options.get('servername')
        database_keys = settings.DATABASES
        
        for database_key in database_keys:
            self.connector = get_connector(database_key)
            database = self.connector.settings
            try:
                self._save_new_backup(database)
            except StorageError as err:
                print(err)

    def _save_new_backup(self, database):
        """
        Save a new backup file.
        """
        print("Backing Up Database:", database['NAME'])
        # Get backup and name
        filename = self.connector.generate_filename(self.servername)
        outputfile = self.connector.create_dump()
        # Apply trans
        # Set file name
        filename = filename
        # Store backup
        outputfile.seek(0)
        self.connector.write_local_file(outputfile, filename)