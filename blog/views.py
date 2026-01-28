from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, SavedPost
from .forms import PostForm
from django.db import connection
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

@never_cache
def post_list(request):
    print('DEBUG: blog.views.post_list called')
    print('USING DATABASE:', connection.settings_dict['NAME'])
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

@never_cache
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    profile = UserProfile.objects.filter(user=post.author).first()  # Fetch author's profile
    
    # Check if the current user has saved this post
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedPost.objects.filter(user=request.user, post=post).exists()
    
    return render(request, 'blog/post_detail.html', {
        'post': post, 
        'profile': profile,
        'is_saved': is_saved
    })

@never_cache
@login_required(login_url='/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = True  # Always publish new posts
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@never_cache
@login_required(login_url='/login/')
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', slug=post.slug)
    return render(request, 'blog/post_form.html', {'form': form})

@never_cache
@login_required(login_url='/login/')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return redirect('post_detail', slug=slug)

@login_required
@require_POST
def save_post(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'This content is saved now',
            'is_saved': True
        })
    
    messages.success(request, 'This content is saved now')
    return redirect('post_detail', slug=slug)

@login_required
@require_POST
def unsave_post(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    SavedPost.objects.filter(user=request.user, post=post).delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Content removed from saved',
            'is_saved': False
        })
    
    messages.info(request, 'Content removed from saved')
    return redirect('post_detail', slug=slug)

@login_required
def saved_content(request):
    saved_posts = SavedPost.objects.filter(user=request.user).select_related('post', 'post__author').order_by('-saved_at')
    posts = [saved_post.post for saved_post in saved_posts]
    return render(request, 'blog/saved_content.html', {'posts': posts})