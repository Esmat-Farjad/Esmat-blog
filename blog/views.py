
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import Comment, Contact, Feature, News, Post, Profile, Project, ProjectImage, Query, Skill, Team, Technology
from hitcount.views import HitCountDetailView
from .forms import (
    CommentForm,
    ContactForm,
      FeatureForm,
    NewsForm,
      TechnologyForm, 
      ProfileUpdateForm, 
      ProjectForm, 
      ProjectImageForm,
    QueryForm,
    SkillForm,
    TeamForm, 
      UserRegistrationForm, 
      BlogPostForm, 
      PostImageForm, 
      UserUpdateForm
)
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.signals import (
    post_save,
    pre_save,
)
# import signals
from django.dispatch import receiver
@receiver(pre_save, sender=User)
def user_pre_save_receiver(instance, sender, *args, **kwargs):
    """
    before saved in the database
    """
    print(instance.username, instance.id)

@receiver(post_save, sender=User)
def user_created_handler(instance, created, sender, *args, **kwargs):
    if created:
        messages.success(instance.username +" created")
        print(instance.username, "created")
# post_save.connect(user_created_handler, sender=User)
# Create your views here.

class PostDetailView(HitCountDetailView):
    model = Post
    template_name = "post_view.html"
    count_hit = True
    

    
def index(request):
    blogs = Post.objects.all().order_by('-created_at')[:3]
    project = Project.objects.all().order_by('-created_at')[:3]
    comments = Comment.objects.select_related('user').order_by('-created_at')[:5]
    skills = Skill.objects.all()
    team = Team.objects.all()
    num_project = project.count()
    num_team = team.count()
    news = News.objects.all().order_by('-created_at')
    
    contact = Contact.objects.all()
    query_form = QueryForm()
    if request.method == 'POST':
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            query_form.save()
            messages.success(request, "Your Query submitted. Thank Your !")
        else:
            messages.error(request, "Oops...something went wrong. please try again...")

   
    context = {
        'comments':comments,
        'blogs':blogs,
        'project':project,
        'team_member':team,
        'query_form':query_form,
        'contact':contact,
        'skills':skills,
        'num_project':num_project,
        'num_team':num_team,
        'news':news
        }
    
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
    user_form = UserRegistrationForm()
    profile_form = ProfileUpdateForm()
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get("username")
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            profile_form.save_m2m()
            messages.success(request, f"{username} registered successfully !")
        else:
            messages.error(request, "Form is not valid Sorry !")
            
    context = {
        'user_form':user_form,
        'profile_form':profile_form
        }
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
    user = request.user
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=user.profile)
    user = User.objects.get(id=user.id)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if Profile.objects.get(user=request.user):
                profile_form.save()
            else:
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
            messages.success(request, 'Profile updated ')
        else:
            messages.error(request, "Invalid Form...")
    
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'user':user
    }
    return render(request, 'forms/update_profile.html', context)

def portfolio(request, pk):
    if pk:
        project = Project.objects.get(id=pk)
        context = {
            'project':project
        }
    return render(request, 'portfolio-details.html',context)

def blog_view(request):
    return render(request, 'blogs_view.html')

def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        image_form = ProjectImageForm(request.POST, request.FILES)
        if project_form.is_valid() and image_form.is_valid():
            pro = project_form.save()
            img = image_form.save(commit=False)
            img.project = pro
            img.save()
            messages.success(request, f"{pro} was added successfully. please upload project images.")

    return redirect('dashboardRoute', 5)

def update_project(request, id):
    project = get_object_or_404(Project,id=id)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Project Updated !")
            return redirect('upload_image', id)
        else:
            messages.error(request, "Something went wrong !")
            return redirect('upload_image',id)
def delete_project(request, id ):
    project = get_object_or_404(Project, id=id)
    if project:
        Project.objects.get(id=id).delete()
        messages.success(request, f"{project} deleted !")
        return redirect('project_list')
def upload_image(request, pk):
    image_form = ProjectImageForm()
    project = Project.objects.get(id=pk)
    project_form = ProjectForm(instance=project)
    if request.method == 'POST':
        image_form = ProjectImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            img = image_form.save(commit=False)
            img.project = project
            img.save()
        else:
            messages.error(request, "Oops...Something went wrong please try again.")

    context={
        'image_form':image_form,
        'project':project,
        'project_form':project_form,
        }
    return render(request, 'forms/upload_image.html', context)

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'projects':projects,
        'posts':posts
    }
    return render(request, 'project_list.html',context)

def change_password(request):
    password_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Your password changed successfully.")
        else:
            messages.error(request, "Invalid Operation.")
    context = {
        'password_form':password_form
    }
    return render(request, 'forms/change_password.html', context)

def user_review(request):
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, "Thanks ! your review submitted.")
        else:
            messages.error(request, "Invalid Operations")
    context = {
        'comment_form':comment_form
    }
    return render(request, 'forms/user_review.html',context)

def add_team(request):
    team_form = TeamForm()
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            user = team_form.cleaned_data.get('user')
            team_form.save()
            messages.success(request, f"{user} added as team memeber successfully.")
        else:
            messages.error(request, "Oops...something went wrong !")
    return redirect('dashboardRoute', 4)

def dashboard(request):
    contact_form = ContactForm()
    skill_form = SkillForm()
    skills = Skill.objects.all()
    info = Contact.objects.all()
    if request.method == 'POST':
        contact_form= ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Contact added successfully ")
            return redirect('dashboardRoute', 1)
        else:
            messages.error(request, "Oops...something went wrong. Please Try Again...")

    context = {
        'skill_form':skill_form,
        'contact_form':contact_form,
        'info':info,
        'skills':skills,
    }
    return render(request, 'admin/dashboard.html', context)

def add_skill(request):
    if request.method == 'POST':
        skill_form = SkillForm(request.POST, request.FILES)
        if skill_form.is_valid():
            skill_form.save()
            messages.success(request, "Skill Added Successfully !")
            return redirect('dashboard')
        else:
            print(skill_form)
            messages.error(request, "Oops...someting went wrong. Please try again.")
            return redirect('dashboard')

def dashboardRoute(request, flag):
    contact_form = None
    skill_form = None
    skills = None
    info = None
    queries = None
    team_form = None
    team_member = None
    news_form = None
    news = News.objects.all().order_by('-created_at')
    project_form = None
    feature_form = None
    technology_form = None
    image_form = None
    features = None
    technologies = None
    project  = None
    if flag == '1':
        contact_form = ContactForm()
        info = Contact.objects.all()
        flag = flag
    elif flag == '2':
        skill_form = SkillForm()
        skills = Skill.objects.all()
        print("HELLO")
        flag = flag
    elif flag == '3':
        queries = Query.objects.all().order_by('-id')
        flag = flag
    elif flag == '4':
        team_form = TeamForm()
        team_member = Team.objects.all()
        flag = flag
    elif flag == '5':
        flag == flag
        project_form = ProjectForm()
        feature_form = FeatureForm()
        technology_form = TechnologyForm()
        image_form = ProjectImageForm()
        features = Feature.objects.all().order_by("-id")
        technologies = Technology.objects.all().order_by("-id")
        project = Project.objects.all().order_by('-created_at')[:5]
    elif flag == '6':
        news_form = NewsForm()
        flag == flag
    context = {
        'skill_form':skill_form,
        'contact_form':contact_form,
        'info':info,
        'skills':skills,
        'flag':flag,
        'queries':queries,
        'team_form':team_form,
        'team_member':team_member,
        'news_form':news_form,
        'news':news,
        'project_form':project_form,
        'feature_form':feature_form,
        'technology_form':technology_form,
        'image_form':image_form,
        'features':features,
        'technologies':technologies,
        'project':project, 
    }
    return render(request, 'admin/dashboard.html', context)

def update_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact_form = ContactForm(instance=contact)
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, instance=contact)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Contact info updated.")
            return redirect("dashboardRoute", 1)
    context = {
        'contact_form':contact_form,
    }
    return render(request, 'admin/update_contact.html', context)   
def delete_contact(request, id):
    if id:
        Contact.objects.filter(id=id).delete()
        messages.success(request, "Contact info has been deleted !")
        return redirect('dashboardRoute', 1)
    
def delete_team(request, id):
    if  id:
        Team.objects.filter(id = id).delete()
        messages.success(request, "Team Member Removed Successfully !")
        return redirect('dashboardRoute', 4 )
def update_team(request, id):
    team = Team.objects.get(id=id)
    team_form = TeamForm(instance=team)
    if request.method == 'POST':
        team_form = TeamForm(request.POST, instance=team)
        if team_form.is_valid():
            team_form.save()
            messages.success(request, "Team member information updated.")
            return redirect('dashboardRoute', 4)
    context = {
        'team_form':team_form,
    }
    return render(request, 'admin/update_team.html',context)

def add_project_feature(request):
    if request.method == 'POST':
        feature_form = FeatureForm(request.POST)
        if feature_form.is_valid():
            feature_form.save()
            messages.success(request, "feature added !")
            return redirect('add_project')
def add_project_technology(request):
    if request.method == 'POST':
        technology_form = TechnologyForm(request.POST)
        if technology_form.is_valid():
            technology_form.save()
            messages.success(request, "Technology added !")
            return redirect('add_project')
def delete_skill(request, id):
    if id:
        Skill.objects.get(id=id).delete()
        messages.success(request, "Skill deleted ! ")
    return redirect('dashboardRoute', 2)
def update_skill(request, id):
    skill = Skill.objects.get(id=id)
    skill_form = SkillForm(instance=skill)
    if request.method == 'POST':
        skill_form = SkillForm(request.POST, request.FILES, instance=skill)
        if skill_form.is_valid():
            skill_form.save()
            messages.success(request, "skill updated !")
            return redirect('dashboardRoute', 2)
        else:
            messages.error(request, "something went wrong !")
    context = {
        'skill_form':skill_form
    }
    return render(request, 'admin/update_contact.html', context)

def like_view(request):
    # X_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if X_forwarded_for:
    #     ip = X_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        ip = "this is an ip address"
        data = {
            'ip':ip,
            'message':'success',
            'status':200
        }
    return JsonResponse(data, safe=False)

def publish_news(request):
   
    if request.method == 'POST':
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            news_form.save()
            messages.success(request, 'News Published !')
            return redirect('dashboardRoute', 6)
        
def delete_news(request, pk):
    if pk:
        News.objects.get(id=pk).delete()
        messages.success(request, "News Deleted !")
        return redirect('dashboardRoute', 6)
def update_news(request, pk):
    if pk:
        news = get_object_or_404(News, id=pk)
        news_form = NewsForm(instance=news)
        if request.method == 'POST':
            news_form = NewsForm(request.POST, instance=news)
            if news_form.is_valid():
                news_form.save()
                messages.success(request, "News Updated !")
                return redirect("dashboardRoute", 6)
        context ={
            'news_form':news_form,
        }
        return render(request, 'admin/update_news.html',context)
def manage_feature_technology(request,pk,slug):
    if slug == 'f':
        pass
    elif slug == 't':
        pass