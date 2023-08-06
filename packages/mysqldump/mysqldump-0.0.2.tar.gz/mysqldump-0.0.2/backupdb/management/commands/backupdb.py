#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
# from django.core.management.base import CommandError
from optparse import make_option
from django.conf import settings
import os
import sys
#import yaml
# from boto.s3.connection import S3Connection
# from boto.exception import S3ResponseError
# from boto.s3.key import Key
from subprocess import Popen, PIPE
# import logging
from time import sleep, time

# log = logging.getLogger(__name__)
"""
Django management command to dump database content and then upload to S3
TODO: Load from config file, refactor. We have hardcoded value of parent object
      and it does not match base object or anything: storage_bucket? file is
      storage_bucket.yaml, devops decided that.
TODO: Rename upload_manager to progress_manager
TODO: Should we be using Popen?
TODO: Get/handle errors from command.
TODO: Decouple action shell commands, use from template?
TODO: Should we name file dumps with DDBB type?
DONE: Rename to dumpdbS3 or something that reflects the fact that is stored
      in S3.
DONE: Do we want to keep a copy? If so, then we need to/could do two uploads,
      one with the regular file name, the other with a timestamp. So only the
      regular name would get overridden and we could always pull the latest by
      name.
"""

HELP = ['Takes a snapshot of the database and upload to S3',
        'Usage:',
        "\t\t\tpython manage.py dumpdbs3 -d default -b dump-test -i",
        "\t\t\tpython manage.py dumpdbs3 -m create -b creates-this-bucket",
        'Config:',
        "With the -C option we can take configuration from a config file."
        ]


class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('-d', '--database', dest="database",default='default',help='Database router id.')
        parser.add_argument('-i', '--incremental', action="store_true",help="Keep an incremental build of all dumps, "
                 "keeping the head always as the latest.")

    def handle(self, *args, **options):

        self.file_name = 'dump.dat'
        self.database = options.get('database') or ''
        database_keys = self.database.split(',') or settings.DATABASES
        

        self.stdout.write("Execute dumpdb command: %s " % self.target)

        # Start initial dump.
        incremental = options['incremental']

        self.start_dump(incremental)

    def load_config(self, path):
        file = open(path, 'r')
        config = file
        # TODO: We have this hardcoded, we should fix it!
        # TODO: This is weak! We need to check for stuff,
        #       catch errors and what nots!!
        config = config['storage_bucket']
        for name in config:
            setattr(self, name, config[name])
        file.close()

    def start_dump(self, incremental):
        dump = self.dump_database()
        if not dump:
            # This usually means that we got an error on the dump process
            # ie: unknown postgress user.
            print("We got not data from dump. Exiting with error.")
            sys.exit(0)

        # We store state, using incremental to track first/second
        # pass. It will affect how we name our dump file.
        self.incremental = incremental

        self.file_path = self.get_file_path(incremental)

        self.save_dump_to_file(self.file_path, dump)

        self.upload_dump_to_S3(self.file_path,
                               self.bucket_name, self.bucket_factory)

    def get_file_path(self, incremental=True):
        # timestamp = incremental and str(time()).split('.')[0] or ""
        timestamp = str(time()).split('.')[0] + '_' if incremental else ""
        return './%s%s' % (timestamp, self.file_name)

    def dump_database(self):
        print("Dump output ready...")
        dumper_method = self.get_dump_method()
        return dumper_method(self.database_settings['NAME'])

    def get_dump_method(self):
        # TODO: Abstract getting settings to method!
        database_engine = self.database_settings['ENGINE']

        # get the right dumper based on DDBB
        dumper_type = self.get_dumper_type(database_engine)
        return getattr(self, dumper_type)

    def save_dump_to_file(self, file_name, dump):
        print("Create dump file...")
        file = open(file_name, 'w+')
        file.write(dump)
        file.close()

    #def upload_dump_to_S3(self, file_name, bucket_name, bucket_factory='get'):
        # print("Pushing %s to S3: %s..." % (file_name, bucket_name))

        # # Sanitize bucket factory method
        # if bucket_factory not in ("get", "create"):
        #     bucket_factory = 'get'

        # conn = S3Connection()

        # try:
        #     # This user requires create permissions, we could just
        #     # change it to use get_bucket if it already exists...
        #     # TODO: Implement command option to use dif method.
        #     bucket_factory = getattr(conn, '%s_bucket' % bucket_factory)
        #     bucket = bucket_factory(bucket_name)
        # except S3ResponseError as e:
        #     self.stdout.write("Error while trying to connect to S3.\n%s" % e)
        #     sys.exit(1)

        # manager = self.upload_manager(self.upload_done)

        # k = Key(bucket)
        # k.key = os.path.basename(file_name)
        # k.set_contents_from_filename(file_name,
        #                              cb=manager, num_cb=20)

    def get_postgresql_psycopg2_dump(self, database):
        # Generate dump file with droptables and all data.
        params = ["sudo", "-u", "postgres",
                  "pg_dump", "-c", database]
        return self.execute_dump(params)

    def get_mysql_dump(self, database):
        params = ['mysqldump', '--user=root',
                  database]
        return self.execute_dump(params)

    def get_sqlite3_dump(self, database):
        pass
        params = ['sqlite3', database,
                  '.dump']
        return self.execute_dump(params)

    def execute_dump(self, params):
        process = Popen(params, stdout=PIPE)
        output = process.communicate()[0]
        return output

    def upload_manager(self, on_done):
        """
        Wrap the progress method so that we can bundle a callback
        on done. We need this because we can't append the callback
        in the progress callback.
        """
        def _upload_progress(loaded=0, total=0, delay=0.4):
            percent = int((loaded*100)/total)
            remainder = 100 - percent
            output = 'Uploading: [{0}{1}] {2}%\r'.format('#' * percent,
                                                         ' ' * remainder,
                                                         percent)
            if percent == 100:
                output = output + '\n'
                delay = 0
            sys.stderr.write(output)
            sleep(delay)
            # We are done!
            if percent == 100:
                on_done()

        return _upload_progress

    def upload_done(self):
        # get the file name and make path
        os.remove(self.file_path)

        if self.incremental:
            print("Uploaded first file.")
            self.start_dump(False)
        else:
            print("Cleaning up. Done!")

    def get_dumper_type(self, engine):
        """
        django.db.backends.postgresql_psycopg2:  psql
        django.db.backends.mysql              :  mysql
        django.db.backends.sqlite3            :  sqlite3
        """
        p = "django.db.backends."
        return 'get_%s_dump' % engine.replace(p, "")