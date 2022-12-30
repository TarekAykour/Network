
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.index,name="create"),
    path("profile/<int:id>",views.profile, name="profile"),
    path("follow/<int:id>",views.follow_user,name="follow"),
    path("unfollow/<int:id>",views.unfollow_user,name="unfollow"),
    path("followingpage",views.following_page,name="followingpage"),

    # API
    path('posts/<int:id>', views.edit, name="post"),
    path("posts/<int:id>/like", views.like, name="like"),
    path("posts/<int:id>/unlike", views.unlike, name="unlike"),
    # path("all_posts", views.all_posts, name="all_posts"),
    path("post/<int:id>",views.post, name="post"),
    path("profile/post/<int:id>", views.post, name="post")
]
