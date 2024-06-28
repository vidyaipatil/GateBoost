from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    year = models.CharField(max_length=15)
    branch = models.CharField(max_length=25)

    def __str__(self):
        return self.user.username
