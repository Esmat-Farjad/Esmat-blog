from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    #Relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=1000)
    view = models.IntegerField(null=True,default=0)
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
    

    
