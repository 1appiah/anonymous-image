from django.db import models

from django.contrib.auth import get_user_model



# Create your models here.

User = get_user_model()

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField( upload_to='media/imgs/',blank=False,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


