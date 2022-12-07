from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
import json
from django.core.files.storage import FileSystemStorage
from .models import User, Data, Follow, Likes


def index(request):
    if request.user.is_authenticated:
        datas = Data.objects.exclude(creater=request.user).all().order_by('-timestamp')
        paginator = Paginator(datas,10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        return render(request, "network/index.html",{
            "post": page_obj,
            # "likes": [like.serialize() for like in datas],
            # "post": datas
            
        })
    paginator = Paginator(Data.objects.all(),10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "network/index.html",{
        "post" : page_obj
        })


def create_post(request, pk):
    if request.method == "POST":
        img = request.FILES.get('upload', None)
        content = request.POST["content"]
        if not content and not img:
            return render(request, "network/create_post.html",{"msg": "Error, post can't be empty","page":pk})
        else:
            data= Data(
            creater = request.user,
            content = content,
            content_img = img
            )
            data.save()
            if pk == 'profile':
                return HttpResponseRedirect(reverse("profile", args=(request.user.id,)))
            else:
                return HttpResponseRedirect(reverse("index"))
    return render(request, "network/create_post.html",{"page": pk})

@login_required
def profile(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")
    user = User.objects.get(id=id)
    if Follow.objects.filter(user=id):
        pass
    else:
        ano = Follow(user=user)
        ano.save()
    if Follow.objects.filter(user=request.user.id):
        pass
    else:
        # creating user follow object 
        another= Follow(user=request.user)
        another.save()
    if request.method == "POST":
        login_user = Follow.objects.get(user=request.user)
        profile_user = Follow.objects.get(user=user)
        # print(request.POST["button"])
        if request.POST["button"] == "unfollow":
            login_user.following.remove(user)
            profile_user.followers.remove(request.user)
        elif request.POST["button"] == "follow":
            login_user.following.add(user)
            profile_user.followers.add(request.user)

        

 
    som=Follow.objects.filter(user=id).values('followers')
    button = "follow"
    for i in som:
        if i["followers"] == request.user.id:
            button = "unfollow"
            break
    # print(button, "but")
    
    # us = User.objects.get(id=3)
    # to remove following 
    # another = Follow.objects.get(id=1)
    # another.followers.add(us)
    # another.following.remove(User.objects.get(id=2))
    # # print(foll) 
    
    # foll= Follow.objects.filter(user=id).values('following')
    # if Follow.objects.filter(user=id):
    #     pass
    # else:
    #     # creating user follow object 
    #     another= Follow(user=user)
    #     another.save()
    
    profile = user
    s = User.objects.get(id=id)
    print(s.user)
    print(s.following.values())
    followers = Follow.objects.filter(user=id).values('followers')
    print(followers)
    following = Follow.objects.filter(user=id).values('following')
    following_count = following.count()
    followers_count = followers.count()
    try:
        if following[0]["following"] == None:
            following_count = 0
        if followers[0]["followers"] == None:
            followers_count = 0
    except Exception:
        following_count = 0
        followers_count= 0
    post = Data.objects.filter(creater=user).all().order_by("-timestamp")
    paginator = Paginator(post,10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    return render(request, "network/profile.html",{
        "profile": profile,
        "login_user": User.objects.get(id=request.user.id),
        "post_count": post.count(),
        "following": following,
        "followers": followers,
        "followers_count": followers_count,
        "following_count":following_count,
        "datas": page_obj,
        "button": button
    })


@csrf_exempt
def likes(request, id):
    data_post = Data.objects.get(id=id)
    lik = Data.objects.only("likes").get(id=id).likes
    if (Likes.objects.filter(liked_content=id)):
        pass
    else:
        Likes.objects.create(liked_content=id)
    if request.method == "GET":
        data=Data.objects.get(id=id)
        return JsonResponse(data.serialize())
    like_data = Likes.objects.get(liked_content=id)
    if request.method == "PUT":
        data = json.loads(request.body)
        in_ = Likes.objects.filter(liked_content=id).values("liked_user")
        in_it="False"
        for i in  in_:
            if i["liked_user"] == request.user.id:
                in_it = "True"
                break
        if in_it == "True":
            like_data.liked_user.remove(request.user)
            data_post.likes = lik-1
            data_post.save()
        else:
            like_data.liked_user.add(request.user)
            data_post.likes = lik+1
            data_post.save()
    return HttpResponse(status=204)
    
@csrf_exempt
def edit(request, id):
    # data = Data.objects.only("content").get(id=id).content
    datas = Data.objects.get(id=id)
    if request.user.id == datas.creater_id:
        if request.method == "GET":
            return JsonResponse(datas.serialize(), safe=False)
        if request.method == "PUT":
            post = Data.objects.get(id=id)
            jdata = json.loads(request.body)
            print(jdata)
            if jdata["del"] == "delete":
                post.delete()
            else:
                post.content=jdata['del']
                # post.content_img=jdata["img"]
                post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse( f"Error! {request.user}, you are not allowed to edit this post", safe=False,status=451)


def following(request, id):
    follow = Follow.objects.filter(user=id).values('following')    
    print(follow)
    datas = Data.objects.filter(creater__in=follow).order_by('-timestamp')
    paginator = Paginator(datas,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "network/following.html", {"datas":page_obj})

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
