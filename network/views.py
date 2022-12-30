import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from requests import post
from .forms import Create_post
from .models import User, Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        message = request.POST["message"]
        if message:
            post = Post(user=request.user,message=message,date=datetime.now())
            post.save()
        else:
            pass
        return HttpResponseRedirect("/")
    else:
        return render(request, "network/index.html", {
            "posts": posts,
            'page_obj':page_obj,
            "pages": range(1 + page_obj.paginator.num_pages),
            
        })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def profile(request,id):
    user = User.objects.get(id=id)
    followers = user.following.all()
    following = user.followers.all()
    posts = Post.objects.filter(user=user).order_by('-date')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/profile.html", {
        "user": user,
        "followers": followers,
        "following": following,
        "posts":posts,
        'page_obj':page_obj,
        "pages": range(1 + page_obj.paginator.num_pages),
        
    })


# follow user
@login_required(login_url='/login')
def follow_user(request,id):
    user = User.objects.get(id=id)
    user.following.add(request.user)
    return HttpResponseRedirect(reverse("profile", args=(id, )))


# unfollow user
@login_required(login_url='/login')
def unfollow_user(request,id):
    user = User.objects.get(id=id)
    user.following.remove(request.user)
    return HttpResponseRedirect(reverse("profile", args=(id, )))


# posts of users the user follows
@login_required(login_url='/login')
def following_page(request):
    following = request.user.following.all()
    posts = Post.objects.filter(user__in=following).order_by('-date')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/followingpage.html", {
        "posts": posts,
        'page_obj':page_obj,
        "pages": range(1 + page_obj.paginator.num_pages),
       
    })


# edit post
@csrf_exempt
@login_required(login_url='/login')
def edit(request,id):
    post = Post.objects.get(user=request.user, pk=id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("message") is not None:
            post.message = data["message"]
        post.save()
        return HttpResponse(status=204)

# like
@csrf_exempt
@login_required(login_url='/login')
def like(request,id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("likes") is not None and request.user not in post.likes.all():
            post.likes.add(request.user)
            status = True
        post.save()
        




# unlike
@csrf_exempt
@login_required(login_url='/login')
def unlike(request,id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("likes") is not None and request.user in post.likes.all():
            post.likes.remove(request.user)
            status = False
        post.save()
        









def post(request,id):
    post = Post.objects.get(id=id)
    if request.method == "GET":
        if request.user in post.likes.all():
            status = True
        else:
            status = False
        return JsonResponse({"post":post.serialize(), "status": status})