"""
URL mappings for the user API.
"""
from django.urls import path

from .views import CreateTokenView


app_name = 'user'

urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token')
]