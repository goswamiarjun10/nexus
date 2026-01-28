from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('post/delete/<slug:slug>/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/save/<slug:slug>/', views.save_post, name='save_post'),
    path('post/unsave/<slug:slug>/', views.unsave_post, name='unsave_post'),
    path('saved/', views.saved_content, name='saved_content'),
]