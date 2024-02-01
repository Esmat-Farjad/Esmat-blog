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
    path('project/update/<str:id>', views.update_project, name='update_project'),
    path('upload/file/<str:pk>', views.upload_image, name='upload_image'),
    path('project/view', views.project_list, name='project_list'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('password/change', views.change_password, name='change_password'),
    path('user/review', views.user_review, name='user_review'),
    path('team/create', views.add_team, name='add_team'),
    path('setting/dashboard', views.dashboard, name='dashboard'),
    path('dashboard/add/skills', views.add_skill, name='add_skill'),
    path('dashboard/route/<flag>', views.dashboardRoute, name='dashboardRoute'),
    path('contact/update/<str:id>', views.update_contact, name='update_contact'),
    path('team/delete/<str:id>', views.delete_team, name='delete_team'),
    path('team/update/<str:id>', views.update_team, name='update_team'),
    path('feature/add', views.add_project_feature, name='add_feature'),
    path('technology/add', views.add_project_technology, name='add_technology'),
    path('contact/delete/<str:id>', views.delete_contact, name='delete_contact'),
    path('skill/delete/<str:id>', views.delete_skill, name='delete_skill'),
    path('skill/update/<str:id>', views.update_skill, name='update_skill'),
]