from celery import shared_task
from core import models
from datetime import datetime, timedelta
from pytz import utc

@shared_task
def delete_expired_url():
   """Delete expired url image."""
   for gen_img in models.TimeGenerateImg.objects.all():
        expiry_date = gen_img.added_at + timedelta(seconds=gen_img.time_of_expiry)

        if datetime.now(utc) > expiry_date:
            gen_img.delete()