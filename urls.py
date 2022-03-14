from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("edit/<int:post_id>", views.edit_post, name="edit"),
    path("likes/<int:post_id>", views.like_post, name="like"),
    path("categories", views.categories, name="categories"),
    path("category_posts/<int:category_id>", views.category_posts,
         name="category_posts"),
    path("profile/<int:user_id>", views.profile, name="profile"),
]
