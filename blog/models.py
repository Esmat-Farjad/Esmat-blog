
from django.db import models
from django.contrib.auth.models import User

from hitcount.models import HitCountMixin
# import signals
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save,
)

# Create your models here.
@receiver(pre_save, sender=User)
def user_pre_save_receiver(instance, sender, *args, **kwargs):
    """
    before saved in the database
    """
    print(instance.username, instance.id)

@receiver(post_save, sender=User)
def user_created_handler(instance, created, sender, *args, **kwargs):
    if created:
        print("Send email to ", instance.username)
    else:
        print(instance.username, "wast just saved")
# post_save.connect(user_created_handler, sender=User)
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
    image = models.ImageField(upload_to="post_images")

    def __str__(self):
        return self.post.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    position = models.CharField(max_length=100, blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(default='default.svg', upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    review = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review
    
class Technology(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name  

class Feature(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Team(models.Model):
    # =======RELATIONS======
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
   

    linkedin = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username



class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Business','Business'),
        ('Education','Education'),
        ('Social','Social'),
        ('Organization','Organization'),
    ]
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  
    # =========RELATIONS==========
    technology = models.ManyToManyField(Technology)
    feature = models.ManyToManyField(Feature)

    link = models.URLField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="project_images")

    def __str__(self) -> str:
        return self.project.name  
    

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.email
    
class Query(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=250)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to="logos")

    def __str__(self):
        return self.name

    
