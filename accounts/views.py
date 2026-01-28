from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, EmailLoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models import Q, Count
from .models import UserProfile
from blog.models import Post

User = get_user_model()


def landing_page(request):
    return render(request, 'landing.html')


# Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')  # or your main content page
    heading = "Create Account"
    subheading = "Join the Nexus community today."
    button_text = "Create Account"
    switch_text = "Already have an account?"
    switch_link = "Sign in"
    switch_url = "/login/"
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('post_list')
        else:
            # Store errors in messages and redirect
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'accounts/auth.html', {
        'form': form,
        'heading': heading,
        'subheading': subheading,
        'button_text': button_text,
        'switch_text': switch_text,
        'switch_link': switch_link,
        'switch_url': switch_url,
    })


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')  # or your main content page
    heading = "Welcome Back"
    subheading = "Sign in to continue to Nexus."
    button_text = "Sign In"
    switch_text = "Don't have an account?"
    switch_link = "Sign up"
    switch_url = "/register/"
    # Check for next param (redirected from protected page)
    if 'next' in request.GET:
        messages.info(request, "To explore Nexus please Sign In")
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user_qs = User.objects.filter(email=email)
                if not user_qs.exists():
                    form.add_error('email', 'No user with this email')
                else:
                    actual_user = user_qs.first()
                    user = authenticate(request, username=actual_user.username, password=password)
                    if user:
                        login(request, user)
                        return redirect('post_list')
                    else:
                        form.add_error(None, 'Invalid credentials')
            except Exception as e:
                form.add_error(None, 'Something went wrong')
        return render(request, 'accounts/auth.html', {
            'form': form,
            'heading': heading,
            'subheading': subheading,
            'button_text': button_text,
            'switch_text': switch_text,
            'switch_link': switch_link,
            'switch_url': switch_url,
        })
    else:
        form = EmailLoginForm()
    return render(request, 'accounts/auth.html', {
        'form': form,
        'heading': heading,
        'subheading': subheading,
        'button_text': button_text,
        'switch_text': switch_text,
        'switch_link': switch_link,
        'switch_url': switch_url,
    })

@login_required
def settings_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()
        banner_picture = request.FILES.get('banner_picture')
        profile_picture = request.FILES.get('profile_picture')
        errors = False
        # Username uniqueness
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, 'This username already exists.')
                errors = True
            else:
                user.username = username
        # Email uniqueness
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'This email already exists.')
                errors = True
            else:
                user.email = email
        if not errors:
            user.save()
            if bio:
                profile.bio = bio
            if banner_picture:
                profile.banner_picture = banner_picture
            if profile_picture:
                profile.profile_picture = profile_picture
            if request.POST.get('remove_banner'):
                profile.banner_picture = None
            if request.POST.get('remove_profile'):
                profile.profile_picture = None
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')
    return render(request, 'accounts/settings.html', {'user': user, 'profile': profile})

def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        profile_picture = request.FILES.get('profile_picture')
        errors = False
        # Username uniqueness
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, 'Username already exists')
                errors = True
            else:
                user.username = username
        # Email uniqueness
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email already exists')
                errors = True
            else:
                user.email = email
        if not errors:
            user.save()
            if profile_picture:
                profile.profile_picture = profile_picture
                profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile, 'posts': posts})


def post_list_view(request):
    print('DEBUG: accounts.views')
    return render(request, 'blog/post_list.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Search users
def search_users(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).distinct()
    
    return render(request, 'accounts/search_results.html', {
        'results': results,
        'query': query
    })

# Public user profile view
def user_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user_obj)
    posts = Post.objects.filter(author=user_obj, published=True)
    post_count = posts.count()
    
    return render(request, 'accounts/user_profile.html', {
        'profile_user': user_obj,
        'profile': profile,
        'posts': posts,
        'post_count': post_count
    })

