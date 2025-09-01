from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/favorite/', views.add_favorite, name='add_favorite'),
    path('blog/<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
]
