
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostImageForm, UserRegistrationForm, BlogPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post

# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request):
    return HttpResponse("Hello and welcome !")
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password !")

    return render(request, 'login.html')
def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"{username} registered successfully !")
            return redirect('signin')
        else:
            form = UserRegistrationForm(request.POST)
    else:
        form = UserRegistrationForm()
    context = {'user_form':form}
    return render(request, 'signup.html', context)
def signout(request):
    logout(request)
    return render(request, 'index.html')

def create_post(request):
    blog_post_form=BlogPostForm()
    image_form=PostImageForm()
    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST)
        if blog_post_form.is_valid():
            blog = blog_post_form.save(commit=False)
            blog.user= request.user
            blog.save()

            post = get_object_or_404(Post, pk=blog.id)
            image_form = PostImageForm(request.POST)
            if image_form.is_valid():
                photo = image_form.save(commit=False)
                photo.post = post
                photo.save()
                messages.success(request, "Post Saved Successfully")
            else:
                return HttpResponse("Formset is Not valid")
        else:
            blog_post_form = BlogPostForm(request.POST)
            image_form = PostImageForm(request.POST)
    context = {
        'blog_post':blog_post_form,
        'post_formset':image_form
    }   
    return render(request, 'post.html', context)

# def create_post_images(request, post):
#     if request.method == 'POST':

#         print("REQUEST COMES IN")
        
#         post = get_object_or_404(Post, pk=post)
#         image_formset = PostImageFormset(request.POST, instance=post, form_kwargs={"post":post})
#         if image_formset.is_valid():
#             image_formset.save()
            
            
#             return redirect('create_post')
#         else:
#             return HttpResponse("Formset is Not valid")