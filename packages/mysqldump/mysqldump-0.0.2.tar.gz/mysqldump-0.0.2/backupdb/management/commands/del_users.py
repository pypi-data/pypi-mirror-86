from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'helps to delete specified user ids'
    def add_arguments(self,parser):
        #arbitary list arguments
        parser.add_argument('user_id', nargs='+', type=int, help='enter valid user id')

    def handle(self, *args, **options):
        """
        delete mentioned user id's
        """
        user_ids = options['user_id']

        for uid in user_ids:
            try:
                user = User.objects.get(pk=uid)
                user.delete()
                self.stdout.write('User "%s (%s)" deleted successfully' %(user.username, uid))
            except User.DoesNotExist:
                self.stderr.write('User id "%s" does not exist' %(uid))