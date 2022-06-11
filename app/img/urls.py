from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter
from img import views

app_name='img'

router = DefaultRouter()
router.register('yours-images', views.ImageViewSet, basename='yours-images')
router.register('upload-image', views.UploadImageViewset, basename='upload-image')


urlpatterns = [
    path('', include(router.urls))
]