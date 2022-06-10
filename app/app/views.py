from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime
import os
import uuid
# Test view
def test(request):


    ext = os.path.basename('filename/sfsad/sfsf.txt')
    print(ext)
    return HttpResponse('siema')