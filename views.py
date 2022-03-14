from django.shortcuts import render

import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import NewPostForm
from .models import *
from . import util


# Displays all posts in reverse chronological order
def index(request):
    posts = Post.objects.order_by("-timestamp").all()
    liked_posts = util.likes_list(request)

    # Paginate posts by 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "video_blog/index.html", {
        "liked_posts": liked_posts,
        "page_obj": page_obj
        })


# Used code provided in project 4
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "video_blog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "video_blog/login.html")


# Used code provided in project 4
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Used code provided in project 4
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "video_blog/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "video_blog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "video_blog/register.html")


# Creates new post from input provided from create.html
@login_required
def create_post(request):
    # Verify that request method and form are valid
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data["content"]
            video = form.cleaned_data["video"]
            category = form.cleaned_data["category"]

            # If category already exists, save the post.
            if Category.objects.filter(name=category):
                category_id = Category.objects.filter(name=category).first()
                category = Category.objects.get(pk=category_id.id)
                post = Post(author=request.user,
                            content=content,
                            video=video,
                            category=category)
                post.save()

            # If category does not already exist, create a new category.
            # Then, display the post.
            else:
                category = Category(name=category)
                category.save()
                post = Post(author=request.user,
                            content=content,
                            video=video,
                            category=category)
                post.save()

            return HttpResponseRedirect(reverse("index"))
        # If the form had errors, display the form again.
        # Keep the user's input in the form.
        else:
            return render(request, "video_blog/create.html", {
                "new_post_form": form
                })

    # Initially display a blank form.
    else:
        return render(request, "video_blog/create.html", {
            "new_post_form": NewPostForm()
            })


# Makes edits to posts based on user's input
@login_required
def edit_post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Get data from form
    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content", "")
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return JsonResponse({
            "content": content,
            })

    # Display an error if the wrong request method is used.
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)


# Tracks whether a user has liked a post
@login_required
def like_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Update whether post is liked or not
    if request.method == "PUT":
        data = json.loads(request.body)
        liked = bool(data.get("liked"))
        if liked:
            request.user.user_likes.add(post)
        else:
            request.user.user_likes.remove(post)

    # Display the updated like count
    return JsonResponse({
        "user_likes": post.user_likes.count()
    })


# Displays a list of post categories
def categories(request):
    return render(request, "video_blog/categories.html", {
            "categories": Category.objects.all()
            })


# Displays all posts within a specific category
def category_posts(request, category_id):
    category = Category.objects.get(pk=category_id)
    liked_posts = util.likes_list(request)

    # Determine posts to be displayed on page
    posts = Post.objects.filter(category=category).order_by("-timestamp")

    # Paginate posts by 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "video_blog/category.html", {
        "category": category,
        "liked_posts": liked_posts,
        "page_obj": page_obj
        })


# Displays all posts by a specific user
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    liked_posts = util.likes_list(request)

    posts = Post.objects.filter(author=profile_user).order_by("-timestamp")

    # Paginate posts by 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "video_blog/profile.html", {
        "liked_posts": liked_posts,
        "page_obj": page_obj,
        })
