from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Executed the the backupdb command"

    def add_arguments(self, parser):
        #positional argument
        parser.add_argument('total', type=int, help='number of user to be created')
        #optional arguments
        parser.add_argument('-p', '--prefix', type=str, help="optional argument -p add username prefix")
        #flag arguments to set boolean value
        parser.add_argument('-a', '--admin', action='store_true', help='to create user as admin')


    def handle(self, *args, **options):
        self.stdout.write("cmd started")
        total = options['total']
        prefix = options['prefix']
        admin = options['admin']

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string())
            else:
                username = get_random_string()
                
            if admin:
                User.objects.create_superuser(username=username, email='', password = '123456789')
            else:
                User.objects.create_user(username=username, email='', password = '123456789')
        self.stdout.write("CMD executed successfully")