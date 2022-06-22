"""
Views used to image options.
"""
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, JsonResponse

from .serializers import (ImageSerializer,
                          TimeGenerateImgSerializer)
from core.models import ImgUpload, ImgThumbnail, TimeGenerateImg, CustomImage

from core.functions import (give_yours_images,
                            give_links_to_images,
                            get_height)

from .tasks import delete_expired_url

class ImageViewSet(viewsets.GenericViewSet):
    """Manage a image in APIs."""
    serializer_class = TimeGenerateImgSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'],
            url_path='yours_images', url_name="yours_images")
    def yours_images(self, request):
        """Return a user images."""
        user_files = give_yours_images(model=ImgUpload,
                                       user=request.user)

        return JsonResponse(user_files)

    @action(detail=False, methods=['get'],
            url_path='links_to_images', url_name='links_to_images')
    def links_to_images(self, request):
        """Return a links to images in dependences from a user group."""
        all_user_links = give_links_to_images(user=request.user,
                                              request=request,
                                              model1=ImgUpload,
                                              model2=ImgThumbnail)

        return Response(all_user_links)

    @action(detail=False, methods=['post'],
            url_path='get_expiry_link', url_name='get_expiry_link')
    def create_expiry_link(self, request):
        """Create a expiry url to image."""
        if not str(request.user.groups.get()) == 'Enterprise':
            return HttpResponse('You have not a permission to do this.')

        serializer = TimeGenerateImgSerializer(data=request.data)
        serializer.user = request.user

        if serializer.is_valid():
            image_type = serializer.validated_data['image_type']
            original_image = serializer.validated_data['original_image']
            time_of_expiry = serializer.validated_data['time_of_expiry']
            qs = ImgUpload.objects.filter
            user_images = list(qs(user=request.user).values_list('id',
                                                                 flat=True))
            if original_image.id not in user_images:  # Validation
                return HttpResponse("You don't have permission to this image.")

            link = CustomImage.make_thumbnail(self,
                                              height=get_height(image_type),
                                              image_type=image_type,
                                              original_image=original_image,
                                              image_path=original_image.image,
                                              model=TimeGenerateImg,
                                              time_of_expiry=time_of_expiry,
                                              user=request.user)
            print(link.id)
            delete_expired_url.apply_async(kwargs={'id': link.id}, countdown=int(time_of_expiry))
            return Response({'expiry_link':
                             request.build_absolute_uri(link.image.url)})


class UploadImageViewset(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Upload image."""
        serializer.save(user=self.request.user)
        user = self.request.user
        CustomImage.create_thumbnail_while_upload(self,
                                                  serializer,
                                                  user=user)
