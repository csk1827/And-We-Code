from django.db import models

# Create your models here.
def get_image_path():
    return os.path.join('photos')
class hfmodel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    #description = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
