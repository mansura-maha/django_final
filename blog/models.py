from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Desi', 'Desi'),
        ('American', 'American'),
        ('Italian', 'Italian'),
        ('Arabian', 'Arabian'),
        ('Greek', 'Greek'),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.blog.title}"


class Rating(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()  # 0-6

    def __str__(self):
        return f"{self.user.username} rated {self.blog.title} as {self.value}"
