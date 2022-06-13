from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime
import os
from django.urls import reverse, reverse_lazy
import uuid
from core import models
from django.contrib.auth.models import User, Group
from django.urls import get_resolver
from PIL import Image
import tempfile
# Test view
def test(request):
    print(request.user.groups.get())
    for i in models.TimeGenerateImg.objects.all():
        print(i.delete())
        break
    return HttpResponse('siema')