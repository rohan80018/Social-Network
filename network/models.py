
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    def serialize(self):
        return{
            "user" : self.user,
            "followers" : self.followers,
            "following" : self.following
        }

class Data(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="data")
    content = models.CharField(max_length=200)
    content_img = models.ImageField(null=True, blank=True, upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add= True)
    likes = models.IntegerField(default=0 )

    def serialize(self):
        return {
            "content": self.content,
            "content_img": str(self.content_img),
            "likes": self.likes,
        }


class Likes(models.Model):
    liked_content = models.IntegerField()
    liked_user = models.ManyToManyField(User,blank=True, related_name="likes_user")

    def serialize(self):
        return {
            "post" : self.liked_content,
            "likes" : str(self.liked_user)
        }