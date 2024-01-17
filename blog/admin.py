from django.contrib import admin
from .models import (
    Post, 
PostImage, 
Profile, 
Comment, 
Technology,
Feature,
Project,
ProjectImage,
Team
)


# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Technology)
admin.site.register(Feature)
admin.site.register(Team)