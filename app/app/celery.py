from celery import Celery
import os
import django
from django.conf import settings
from django.apps import apps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


app = Celery('app')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = 'Europe/Warsaw'
app.conf.enable_utc = True

app.conf.beat_schedule = {
    'every-minute': {
        'task': 'img.tasks.delete_expired_url',
        'schedule': 1}
    }

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])