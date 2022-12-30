from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, related_name='followers', symmetrical=False)
   


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT, default='',null=True)
    message = models.TextField()
    date = models.DateTimeField()
    likes = models.ManyToManyField(User,blank=True,null=True,related_name="posts")
    
   

    def serialize(self):
            return {
            "id": self.id,
            "user": self.user.username,
            "likes": [user.id for user in self.likes.all()],
            "message": self.message,
            "date": self.date.strftime("%b %d %Y")
        }



    


