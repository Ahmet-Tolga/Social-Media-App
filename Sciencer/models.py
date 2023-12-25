from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
import time as tm
user=get_user_model()

# Create your models here.

class profile(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    proile_image=models.ImageField(upload_to="profile_images",default="blank-profile-picture.png")
    location=models.CharField(max_length=100,blank=True)
    job=models.CharField(max_length=120,blank=True)
    def __str__(self):
        return str(self.user)
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to="post-images")
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    number_of_likes=models.IntegerField(default=0)
    category=models.ForeignKey(Category,related_name="Posts",on_delete=models.CASCADE,blank=False)

    def __str__(self):
        return str(self.user)
    def get_name(self):
        return str(self.user)
class like(models.Model):
    post_id=models.CharField(max_length=600)
    username=models.CharField(max_length=100)

    def __str__(self):
        return str(self.username)
class follewerCounts(models.Model):
    follwer=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)
class Message(models.Model):
    
    message=models.CharField(max_length=100000)
    date=models.CharField(max_length=200)
    user=models.CharField(max_length=100)
    post_id=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.user)




