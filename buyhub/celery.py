from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'buyhub.settings')

app = Celery('buyhub')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Dhaka')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-10AM': {
        'task': 'accounts.tasks.send_mail_func',
        # 'schedule': crontab(minute='*/1'),
        'schedule': crontab(hour='10', minute='0'),
    }
}
# ...

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
