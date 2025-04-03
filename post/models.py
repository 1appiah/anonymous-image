from django.db import models
from django.contrib.auth.models import User
from users.models import NewUser
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(NewUser,related_name='blog_post',blank=True)
    total_likes = models.PositiveIntegerField(null=True)

    def __str__(self) -> str:
        return self.title
    def  save(self, *args, **kwargs):

       super().save(*args, **kwargs) # Call the real save() method
    

class Comments(models.Model):
    postc = models.ForeignKey('Post', on_delete=models.CASCADE, null=True,related_name='com')
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField( auto_now_add=True)
    body = models.TextField()



    