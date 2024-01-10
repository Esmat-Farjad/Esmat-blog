
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, PostImage

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "px-3 w-full py-3 outline-none border border-sky-500 rounded focus:border-red-500"
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

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']

        widgets = {
            'title': forms.TextInput(attrs={
                'class':'form-control shadow-none',
                'required':True }),
            'text': forms.Textarea(attrs={
                'class':'form-control shadow-none',
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
            'image': forms.FileInput(attrs={
                'type':'file',
                'required': True   
                })
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

    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = ""
            
        

    


