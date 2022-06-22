"""
Backgroung django celery beat tasks.
"""
from celery import shared_task
from core import models
from datetime import datetime, timedelta
import time

from core.models import TimeGenerateImg

# @shared_task
# def delete_expired_url():
#     """Delete expired url image."""
#     for gen_img in models.TimeGenerateImg.objects.all():
#         expiry_date = gen_img.added_at + \
#                       timedelta(seconds=gen_img.time_of_expiry)

#         if datetime.now() > expiry_date:
#             gen_img.image.delete()
#             gen_img.delete()


@shared_task(name="sum_two_numbers")
def add(x, y):

    return x + y


@shared_task
def delete_expired_url(id):
    """Delete expired url image."""
    img = TimeGenerateImg.objects.get(id=id)
    img.image.delete()
    img.delete()
