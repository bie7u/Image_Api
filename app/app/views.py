from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime
import os
from django.urls import reverse, reverse_lazy
import uuid
from core import models
# Test view
def test(request):
    reverse('img:yours-images-list')
    for i in models.ImgUpload.objects.all():
        print(os.path.exists(i.image.path))
        print(i.image.path)

    ext = os.path.basename('filename/sfsad/sfsf.txt')
    print(ext)
    return HttpResponse('siema')