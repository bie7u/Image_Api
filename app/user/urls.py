"""
URL mappings for the user API.
"""
from django.urls import path

from .views import CreateTokenView, ManagerUserViewset


app_name = 'user'

urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token'),
    path('user_group/', ManagerUserViewset.as_view(), name='user-group')
]