from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime
# Test view
def test(request):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    print(dt)
    print(get_user_model().__doc__)
    return HttpResponse('siema')