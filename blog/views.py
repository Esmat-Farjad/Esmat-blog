
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
        else:
            form = UserRegistrationForm(request.POST)
    else:
        form = UserRegistrationForm()
    context = {'user_form':form}
    return render(request, 'signup.html', context)