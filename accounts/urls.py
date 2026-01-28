from django.urls import path
from . import views
from blog.views import post_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', post_list, name='post_list'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_users, name='search_users'),
    path('user/<str:username>/', views.user_profile_view, name='user_profile'),
    path('settings/', views.settings_view, name='settings'),
]