
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, PostImage, Project, Feature, Technology, ProjectImage

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
        fields = "__all__"
        exclude = ('created_at','id','image')   
        widgets = {
            'technology': forms.SelectMultiple(attrs={'multiple':'multiple'}),
            'feature': forms.SelectMultiple(attrs={'multiple':'multiple'}),
            'description':forms.Textarea(attrs={'rows':4})
               
        } 
    # def __init__(self, *args, **kwargs):
    #     super(ProjectForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = "form-control shadow-none mt-0 "

            
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

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

# select multiple file 
# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True
# class MultipleFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('widget', MultipleFileInput())
#         super().__init__(*args, **kwargs)
    
#     def clean(self, data, initial=None):
#         single_file_clean = super().clean
#         if isinstance(data, (list, tuple)):
#             result = [single_file_clean(d, initial) for d in data]
#         else:
#             result = single_file_clean(data, initial)
#         return result
# class ProjectImageForm(forms.ModelForm):
#     image = MultipleFileField()
#     class Meta:
#         model = ProjectImage
#         fields = ['image']
        
    


