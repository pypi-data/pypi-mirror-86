import tempfile
from django.conf import settings

TMP_FILE_MAX_SIZE = getattr(settings, 'DBBACKUP_TMP_FILE_MAX_SIZE', 10 * 1024 * 1024)
TMP_FILE_READ_SIZE = getattr(settings, 'DBBACKUP_TMP_FILE_READ_SIZE', 1024 * 1000)

CONNECTORS = getattr(settings, 'DATABASES', {})
DATABASES = getattr(settings, 'DATABASES', list(settings.DATABASES.keys()))
TMP_DIR = '/home/nandha/Desktop/'