from django.contrib.auth import authenticate

from .models import *


def likes_list(request):
    posts = Post.objects.order_by("-timestamp").all()
    liked_posts = []
    if request.user.is_authenticated:
        for post in posts:
            if request.user.user_likes.filter(id=post.id).exists():
                liked_posts.append(post)
    else:
        liked_posts = []
    return liked_posts
