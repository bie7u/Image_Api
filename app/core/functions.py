"""
All custom functions used in project.
"""

def give_yours_images(model, user): # model = ImgUpload
    """Return all user images with links."""
    queryset = model.objects.filter(user=user)
    user_files = {}

    for img in queryset:
        name_of_file = img.image.path.split('__file_name--')[1]
        user_files[f'image_id={img.id}'] = name_of_file

    return user_files

def give_links_to_images(user, request, model1, model2): # model1 = ImgUpload, model2 = ImgThumbnail
    """Render a json file with links to images."""
    all_links = {}
    image_id = None

    for i in model1.objects.filter(user=user):
        image_links = {}
        image_id = f"image_id: {i.id}"

        original_image = request.build_absolute_uri(i.image.url)
        if str(user.groups.get()) in ['Premium', 'Enterprise']:
            image_links['original_image'] = original_image

        thumbnail = model2.objects.filter(user=i.user, original_image_id=i.id)

        for thumb in thumbnail:
            if thumb.image_type == '2':
                image_links['200px_thumbnail'] = request.build_absolute_uri(thumb.image.url)
            elif thumb.image_type == '3':
                image_links['400px_thumbnail'] = request.build_absolute_uri(thumb.image.url)
        all_links[image_id] = [image_links]

    return all_links

def get_height(image_type):
        """Return a height - image type."""
        if image_type == '1':
             return None
        elif image_type == '2':
            return 200
        elif image_type == '3':
            return 400
