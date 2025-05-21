from django.db import models
from django.conf import settings


class Profile(models.Model):
    # info   
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_photo=models.ImageField(upload_to="images",blank=True,null=True)
    bio=models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    

    