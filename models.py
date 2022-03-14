from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_likes = models.ManyToManyField("Post", blank=True,
                                        related_name="user_likes")


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE,
                               related_name="posts")
    video = models.FileField(upload_to="videos/", null=True)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name="categories",
                                 default=None,
                                 null=True,
                                 blank=True)


class Category(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
