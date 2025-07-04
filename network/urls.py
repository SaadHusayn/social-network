
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPost", views.create_post, name="createPost"),
    path("user/<str:username>", views.user_profile, name="userProfile"),
    path("following", views.following, name="following"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name="like"),
    path("editPost", views.editPost, name="editPost"),
    path("getComments", views.getComments, name="getComments"),
    path("addComment", views.addComment, name="addComment"),
]
