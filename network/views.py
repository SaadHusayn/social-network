from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Comment
from .forms import PostForm, RegisterForm
import json
from .util import get_page_obj

def index(request):
    page_obj = get_page_obj(request, Post.objects.all().order_by('-created_at'))
    return render(request, "network/index.html", {"form": PostForm(), "page_obj":page_obj})


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"form": form, "message": "Passwords must match."}
            )
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=password
                )
                # Optional fields
                user.bio = form.cleaned_data.get("bio", "")
                profile_picture = form.cleaned_data.get("profile_picture")
                if profile_picture:
                    user.profile_picture = profile_picture
                user.save()
            except IntegrityError:
                return render(
                    request, "network/register.html", {"form": form, "message": "Username already taken."}
                )
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/register.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "network/register.html", {"form": form})

@login_required
def create_post(request):
    if request.method == "POST":
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.creator = request.user
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {"form": postForm, "page_obj":get_page_obj(request, Post.objects.all().order_by('-created_at'))})
    else:
        return HttpResponseNotFound('not allowed :(')


def user_profile(request, username):
    try:
        user = User.objects.get(username = username)
    except:
        return HttpResponseNotFound('not allowed :(')

    page_obj = get_page_obj(request, user.posts.all().order_by('-created_at'))
    
    return render(request, 'network/profile.html',{"userData":user, "page_obj":page_obj})

@login_required
def follow(request):
    if request.method != "POST":
        #redirect to the home page
        return HttpResponseRedirect(reverse("index"))

    user1 = request.user
    user2 = User.objects.get(pk = request.POST["user2ID"])
    toFollow = int(request.POST["toFollow"])

    #if toFollow is true, user1 follows user2
    #if toFollow is false, user1 unfollows user2
    if toFollow:
        if not user2 in user1.following.all():
            user2.add_follower(user1)
    else:
        if user2 in user1.following.all():
            #user1 is unfollowing user2
            user1.following.remove(user2)
    
    return HttpResponseRedirect(reverse("userProfile", args=(user2.username, )))


@login_required
def following(request):
    posts = Post.objects.none()
    for user in request.user.following.all():
        posts = posts | user.posts.all()

    page_obj = get_page_obj(request, posts.order_by('-created_at'))
    
    return render(request, 'network/following.html',{"page_obj":page_obj})

@login_required
def like(request):
    if request.method != "PUT":
        return HttpResponseNotFound('Error: only put request is allowed')
    
    data = json.loads(request.body)
    post = Post.objects.get(pk = data["postID"])
    isLike = data["like"]

    if isLike:
        post.liked_by.add(request.user)
    else:
        post.liked_by.remove(request.user)
    
    return HttpResponse(status=200)

@login_required
def editPost(request):
    if request.method != "PUT":
        return HttpResponseNotFound('Error: only put request is allowed')
    
    data = json.loads(request.body)
    post = Post.objects.get(pk = data["postID"])
    postContent = data["postContent"]

    if post.creator == request.user:
        post.postContent = postContent
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse('Error: A user can only edit their own posts!', status=404)


def getComments(request):
    if request.method != "GET":
        return HttpResponseNotFound('Error: only get request is allowed')
    
    postID = request.GET["postID"]
    PostObj = Post.objects.get(pk = postID)
    comments = PostObj.comments.all()
    comments = comments.order_by('-created_at')

    return JsonResponse([comment.serialize() for comment in comments], safe=False)

@login_required
def addComment(request):
    if request.method != "POST":
        return HttpResponseNotFound('Error: only post request is allowed')
    
    data = json.loads(request.body)
    post = Post.objects.get(pk = data["postID"])
    content = data["content"]

    comment = Comment(content = content, writer = request.user, post = post)
    comment.save()

    return HttpResponse(status=200)