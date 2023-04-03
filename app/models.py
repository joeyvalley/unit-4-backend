from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=f'avatars/', blank=True, null=True, max_length=9999)
    posts = ArrayField(models.IntegerField(), blank=True, null=True)
    likes = ArrayField(models.IntegerField(), blank=True, null=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'posts/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = ArrayField(models.IntegerField(),
                          blank=True, null=True, default=list)

    class Meta:
        ordering = ['author']

    def __str__(self):
        return f'{self.caption} by {self.author}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text} by {self.author} on {self.post}'
