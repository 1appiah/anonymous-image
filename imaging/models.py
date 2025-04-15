from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from cloudinary_storage.storage import MediaCloudinaryStorage




# Create your models here.

User = get_user_model()

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #image = CloudinaryField('image', blank=False, null=True)
    image = models.ImageField(null=True,blank=True,upload_to='image/',storage=MediaCloudinaryStorage())

    timestamp = models.DateTimeField(auto_now_add=True)


