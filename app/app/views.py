from django.contrib.auth import get_user_model
from django.http import HttpResponse

def test(request):
    print(get_user_model().__doc__)
    return HttpResponse('siema')