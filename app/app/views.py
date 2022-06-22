from django.http import HttpResponse
from img.tasks import add
from datetime import datetime

def test(request):
    a = datetime.now()
    for i in range(1, 100000):

        add.apply_async(kwargs={'x': i, 'y':0}, countdown=10)

    return HttpResponse('Siema')