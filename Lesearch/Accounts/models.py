from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 
# Create your models here.
#ユーザ情報のDB情報
class UserInfo(models.Model):
    consultantName = models.CharField(max_length=200)
    clientName1 = models.CharField(max_length=200,null=True)
    clientName2 = models.CharField(max_length=200,null=True)
    clientName3 = models.CharField(max_length=200,null=True)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followings')
