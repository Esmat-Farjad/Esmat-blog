
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CommentForm, UserRegistrationForm, BlogPostForm, PostImageForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from hitcount.views import HitCountDetailView

# Create your views here.
class PostDetailView(HitCountDetailView):
    model = Post
    template_name = "post_view.html"
    count_hit = True
    

def index(request):
    blogs = Post.objects.all().order_by('-created_at')[:3]
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, "Your review posted successfully ! Thanks...")
        else:
            comment_form = CommentForm(request.POST)
            messages.error(request, "Oops...Something went wrong !")
    
    context = {'blogs':blogs,'comment_form':comment_form}
    
    return render(request, 'index.html', context)

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

    return render(request, 'forms/signin.html')
def signup(request):
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"{username} registered successfully !")
            
        else:
            messages.error(request, "Form is not valid Sorry !")
            form = UserRegistrationForm(request.POST)
    else:
        form = UserRegistrationForm()
    context = {'user_form':form}
    return render(request, 'forms/signup.html', context)
def signout(request):
    logout(request)
    return render(request, 'index.html')

def create_post(request):
    blog_post_form=BlogPostForm()
    image_form = PostImageForm()

    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST)
        image_form = PostImageForm(request.POST, request.FILES)
        if blog_post_form.is_valid() and image_form.is_valid():
            blogPost = blog_post_form.save(commit=False)
            blogPost.user = request.user
            blogPost.save()

            imagePost = image_form.save(commit=False)
            imagePost.post = blogPost
            imagePost.save()
            messages.success(request, "Your Post created successfully !")
        else:
            messages.error(request, "Forms are invalid !")
    recent_post = Post.objects.filter(user=request.user).order_by('-created_at')[:5]      
    context = {
        'post_form':blog_post_form,
        'image_form':image_form,
        'recent_post':recent_post
    }   
    return render(request, 'forms/post_form.html', context)

def post_view(request, pid):
    post = Post.objects.get(id=pid)
    all_posts = Post.objects.all().order_by('-created_at')
    context = {'post':post, 'all_posts':all_posts}
    return render(request, 'post_view.html', context)

def update_profile(request):
    return render(request, 'profile.html')

def portfolio(request):
    return render(request, 'portfolio-details.html')