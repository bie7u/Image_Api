from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime, timedelta
import os
from django.urls import reverse, reverse_lazy
import uuid

from pytz import timezone, utc
from core import models
from django.contrib.auth.models import User, Group
from django.urls import get_resolver
from PIL import Image
import tempfile
# Test view
def test(request):

    models.TimeGenerateImg.objects.all()
    for i in models.TimeGenerateImg.objects.all():
        a = i.added_at + timedelta(seconds=i.time_of_expiry)
        print(a)
        print(datetime.now(utc))


    return HttpResponse('siema')