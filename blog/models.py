from django.db import models
from django.contrib.auth.models import User

from hitcount.models import HitCountMixin


# Create your models here.

class Post(models.Model, HitCountMixin):
    #Relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=1000)
    view = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
 
    
class PostImage(models.Model):
    #Relationships
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="post_images")

    def __str__(self):
        return self.post.title
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    position = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    RATE_CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3,','3'),
        ('4','4'),
        ('5','5')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rate = models.IntegerField(choices=RATE_CHOICES)
    review = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

    
