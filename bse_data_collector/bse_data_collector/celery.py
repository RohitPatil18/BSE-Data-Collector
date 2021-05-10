from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from bse_data_collector import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bse_data_collector.settings')

app = Celery('bse_data_collector')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configuring schedules tasks
app.conf.beat_schedule = {
    'tsk-download-bhavcopy-zip' : {
        'task' : 'bhavcopy.tasks.download_bhavcopy_zip',
        'schedule' : crontab(minute=00, hour=18)
    }
}