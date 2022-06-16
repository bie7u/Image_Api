from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import os
from django.urls import reverse, reverse_lazy
import uuid
from app.settings import ALLOWED_HOSTS
from pytz import timezone, utc
from core import models
from django.contrib.auth.models import User, Group
from django.urls import get_resolver
from PIL import Image
import tempfile
# Test view
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
import sys
from core import models

def test(request):
    b = 2 + \
        2
    print(b)
    return HttpResponse('fsd')
