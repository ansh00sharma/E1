from django.core.exceptions import ValidationError
import os

def allowOnlyImagesValidator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg','.png','.webp','.jepg']

    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File extension. Allowed extension : " +str(valid_extensions))