
from django import forms
from .models import CustomUser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(image, max_size=(800, 800)):
    try:
        img = Image.open(image)

        if img.mode == 'RGBA':
            img = img.convert('RGB')

        img.thumbnail(max_size)

        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG', quality=70)

        return InMemoryUploadedFile(
            output_buffer,
            'ImageField',  # Field name in your model
            f'{image.name.split(".")[0]}_compressed.jpg',  # Adjust the filename as needed
            'image/jpeg',  # MIME type
            img.tell, None
        )
    except Exception as e:
        # Handle any exceptions that might occur during image processing
        print(f"Error compressing image: {str(e)}")
        return None





class ImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_pic',)


    def save_profile_pic(self, user_id):
        user = CustomUser.objects.get(pk=user_id)
        profile_picture = self.cleaned_data['profile_pic']
        compressed_profile_picture = compress_image(profile_picture)
        user.profile_pic = compressed_profile_picture
        user.save()

