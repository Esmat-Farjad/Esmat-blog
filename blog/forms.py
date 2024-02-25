
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Contact, News, Post, PostImage, Profile, Project, Feature, Query, Skill, Team, Technology, ProjectImage

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','password1','password2']
        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'Enter a unique username...'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control shadow-none mt-0 "


    def clean_email(self):
        """check if email already exist"""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(f"{email} is already exists. please pick another")
        return email
    def clean_username(self):
        """check if username already exist"""
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError(f"{username} is already exists. please pick another")
        return username
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user',)
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'form-control shadow-none',
                'required':True }),
            'text': forms.Textarea(attrs={
                
                'rows':6,
                'required':True
                })
        }
        
class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        field = "__all___"
        exclude = ('post',)
        widgets = {
            'image': forms.FileInput(attrs={'type':'file'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        field = "__all__"
        exclude = ('user','created_at',)
        labels = {'review':'Descriptions'}
        widgets = {
            'review': forms.Textarea(
                attrs={
                    'class':'px-3 w-96 py-3 outline-none border-b border-sky-500 rounded focus:border-red-500',
                    'rows':3,
                    'placeholder':'Type your review...'
                    }
            ),
            'rate':forms.Select(
                attrs={
                    'class':'px-3 w-32 py-3 outline-none border border-sky-500 rounded focus:border-red-500'
                    })
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','category','link','feature','technology','description']
          
        widgets = {
            'technology': forms.SelectMultiple(attrs={'multiple':'multiple'}),
            'feature': forms.SelectMultiple(attrs={'multiple':'multiple'}),
            'description':forms.Textarea(attrs={'rows':4})
               
        }         
class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = "__all__"
        exclude = ("project",)
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control shadow-none mt-0',
                'placeholder':'Enter features..'
                })
        }
class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = "__all__"
class ProjectImageForm(forms.ModelForm):
    
    class Meta:
        model = ProjectImage
        fields = ['image']
    
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"  
class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = "__all__"   
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder':'Your Message...',
                'rows':5
                }),
            'name': forms.TextInput(attrs={'placeholder':'Full Name'}),
            'email': forms.TextInput(attrs={'placeholder':'Email'}),
            'subject': forms.TextInput(attrs={'placeholder':'Subject'}),
        }  
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        
    


