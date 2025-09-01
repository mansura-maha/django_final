from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog, Profile, Favorite, Rating
from .forms import ProfileForm, BlogForm, RatingForm


# Home page with search and filters 
def home(request):
    blogs = Blog.objects.annotate(avg_rating=Avg('ratings__value')).order_by('-created_at')
    category = request.GET.get('category')
    author_id = request.GET.get('author')
    date = request.GET.get('date')
    search = request.GET.get('search')

    if category and category != 'All':
        blogs = blogs.filter(category=category)
    if author_id and author_id != 'All':
        blogs = blogs.filter(author__id=author_id)
    if date:
        blogs = blogs.filter(created_at__date=date)
    if search:
        blogs = blogs.filter(Q(title__icontains=search) | Q(body__icontains=search))

    authors = Profile.objects.filter(is_author=True)
    categories = ['Desi', 'American', 'Italian', 'Arabian', 'Greek']

    return render(request, 'blog/home.html', {
        'blogs': blogs,
        'authors': authors,
        'categories': categories,
    })


# User registration (with Profile creation)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create profile for the new user
            Profile.objects.create(user=user)

            messages.success(request, '🎉 Your account has been created! You can log in now.')
            return redirect('login')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'blog/login.html')


# User logout
def user_logout(request):
    logout(request)
    return redirect('home')


# User profile
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {'form': form})


# Create blog (author only)
@login_required
def create_blog(request):
    if not request.user.profile.is_author:
        messages.error(request, 'Only authors can create blogs')
        return redirect('home')
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created')
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})


# Blog detail view with average rating
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    rating_form = RatingForm()
    avg_rating = blog.ratings.aggregate(Avg('value'))['value__avg'] or 0
    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'rating_form': rating_form,
        'avg_rating': avg_rating
    })


# Add blog to favorites
@login_required
def add_favorite(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    Favorite.objects.get_or_create(user=request.user, blog=blog)
    messages.success(request, 'Added to favorites!')
    return redirect('blog_detail', pk=pk)


# Add or update rating for a blog
@login_required
def add_rating(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            user=request.user,
            blog=blog,
            defaults={'value': form.cleaned_data['value']}
        )
        messages.success(request, 'Rating submitted!')
    return redirect('blog_detail', pk=pk)


# Author detail page
def author_detail(request, pk):
    author = get_object_or_404(Profile, pk=pk)
    blogs = Blog.objects.filter(author=author.user)
    return render(request, 'blog/author_detail.html', {'author': author, 'blogs': blogs})
