from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Profile(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=1000, blank=True, null=True)
    posts = ArrayField(models.IntegerField(), blank=True, null=True)
    likes = ArrayField(models.IntegerField(), blank=True, null=True)
    dislikes = ArrayField(models.IntegerField(), blank=True, null=True)
    follow = ArrayField(models.IntegerField(), blank=True, null=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.CharField(max_length=100, blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Likes = models.IntegerField(default=0)
    liked_by = ArrayField(models.IntegerField(),
                          blank=True, null=True, default=list)
    dislike_by = ArrayField(models.IntegerField(),
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


# class Follow(models.Model):
#     from_user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='from_user')
#     to_user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='to_user')
#     created_at = models.DateTimeField(auto_now_add=True)
#     followers = ArrayField(models.IntegerField(), blank=True, null=True)

#     def __str__(self):
#         return f'{self.from_user} follows {self.to_user}'
