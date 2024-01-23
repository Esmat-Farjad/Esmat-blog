from django.urls import path
from blog import views
from .views import PostDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('post/create', views.create_post, name='create_post'),
    path('post/view/<pid>', views.post_view, name='post_view'),
    path('post/<int:pk>/<str:slug>', PostDetailView.as_view(), name='post_view'),
    path('profile/update', views.update_profile, name='profile'),
    path('portfolio/<str:pk>', views.portfolio, name='portfolio'),
    path('post/view/', views.post_view, name='post_view'),
    path('blogs/view/', views.blog_view, name='blog_view'),
    path('project/add/', views.add_project, name='add_project'),
    path('upload/file/<str:pk>', views.upload_image, name='upload_image'),
    path('project/view', views.project_list, name='project_list'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('password/change', views.change_password, name='change_password'),
    path('user/review', views.user_review, name='user_review'),
    path('team/create', views.add_team, name='add_team'),
    path('setting/dashboard', views.dashboard, name='dashboard'),
    path('dashboard/add/skills', views.add_skill, name='add_skill'),
]