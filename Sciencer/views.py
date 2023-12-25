from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import profile,Post,like,Category,follewerCounts,Message
from django.contrib.auth.decorators import login_required
import time as tm

# Create your views here.
def calc_time():
    time=tm.localtime()
    day=str(time.tm_mday)
    month=str(time.tm_mon)
    year=str(time.tm_year)
    hour=str(time.tm_hour)
    minute=str(time.tm_min)
    if(len(day)==1):
        day="0"+day
    if(len(month)==1):
        month="0"+month
    if(len(hour)==1):
        hour="0"+hour
    if(len(minute)==1):
        minute="0"+minute
    return "{}.{}.{}  {}:{}".format(day,month,year,hour,minute)

@login_required(login_url="login")
def index(request):
    username=request.GET.get("username")
    user_object=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(user=user_object)
    Category_list=Category.objects.all()
    post_list=Post.objects.all()
    return render(request,"index.html",{"user_profile":user_profile,"posts":post_list,"Category":Category_list})
@login_required(login_url="login")
def upload(req):
    if(req.method=="POST"):
        user=req.user.username
        image=req.FILES.get("image-upload")
        caption=req.POST["caption"]
        category=req.POST["category"]
        new_category=Category.objects.filter(name=category).first()
        if(image==None):
            new_post=Post.objects.create(user=user,image="sciencer.png",caption=caption,category=new_category)
        else:
            new_post=Post.objects.create(user=user,image=image,caption=caption,category=new_category)
        new_post.save()
        return redirect("/")
    return redirect("/")
def signup(req):
    if req.method=="POST":
        username=req.POST["name"]
        password=req.POST["password"]
        password_again=req.POST["password_again"]
        if(password==password_again):
            if(User.objects.filter(username=username)):
                messages.info(req,"Username must be special please find another")
                return redirect("signup")
            user=User.objects.create_user(username=username,password=password)
            user.save()
            #log user in and redirect to settings page
            user_login=auth.authenticate(username=username,password=password)
            auth.login(req,user_login)
            #create a profile
            user_model=User.objects.get(username=username)
            new_profile=profile.objects.create(user=user_model)
            new_profile.save()
            return redirect("login")
        else:
            messages.info(req,"passwords must be equal")
            return redirect("signup")
    else:
        return render(req,"sign_up.html")
def login_page(req):
    if(req.method=="POST"):
        username=req.POST["username"]
        password=req.POST["password"]
        
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(req,user)
            return redirect("/")
        else:
            messages.info(req,"There is no user like this \ntry to signup")
            return redirect("login")
    else:
        return render(req,"Login.html")
@login_required(login_url="login")
def logout(req):
    auth.logout(req)
    return redirect("login")
@login_required(login_url="login")
def settings(req):
    user_profile=profile.objects.get(user=req.user)
    if(req.method=="POST"):
        if(req.FILES.get("image")==None):
            image=user_profile.proile_image
            bio=req.POST["bio"]
            job=req.POST["job"]
            location=req.POST["location"]
            user_profile.proile_image=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.job=job
            user_profile.save()
        if (req.FILES.get("image")!=None):
            image=req.FILES.get("image")
            bio=req.POST["bio"]
            job=req.POST["job"]
            location=req.POST["location"]
            user_profile.bio=bio
            user_profile.proile_image=image
            user_profile.location=location
            user_profile.job=job
            user_profile.save()
        return redirect("settings")
    return render(req,"setting.html",{"user_profile":user_profile})
@login_required(login_url="login")
def like_post(req):
    username=req.user.username
    post_id=req.GET.get("post_id")

    post=Post.objects.get(id=post_id)

    like_filter=like.objects.filter(post_id=post_id,username=username).first()
    if(like_filter==None):
        new_like=like.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.number_of_likes+=1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.number_of_likes-=1
        post.save()
        return redirect("/")
@login_required(login_url="login")
def profile_page(req,pk):
    user_object=User.objects.get(username=pk)
    user_profile=profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=pk)
    user_post_length=len(user_post)
    follower=req.user.username
    user=pk
    if(follewerCounts.objects.filter(follwer=follower,user=user).first()):
        button_text="unfollow"
    else:
        button_text="follow"
    user_followers=len(follewerCounts.objects.filter(user=pk))
    user_following=len(follewerCounts.objects.filter(follwer=pk))
    context={"user_object":user_object,"user_profile":user_profile,"user_post":user_post,"user_post_length":user_post_length,"button_text":button_text,"followers":user_followers,"following":user_following}

    return render(req,"profile.html",context)
@login_required(login_url="login")
def follow(req):
    if(req.method=="POST"):
        follower=req.POST["follower"]
        user=req.POST["user"]
        if(follewerCounts.objects.filter(follwer=follower,user=user)).first():
            delete_follower=follewerCounts.objects.get(follwer=follower,user=user)
            delete_follower.delete()
            return redirect("/profile/"+user)
        else:
            new_follower=follewerCounts.objects.create(follwer=follower,user=user)
            new_follower.save()
            return redirect("/profile/"+user)
    else:
        return redirect("/")
@login_required(login_url="login")
def show(req,pk):
    post_list=Post.objects.filter(category=pk)
    Category_list=Category.objects.all()
    user_object=User.objects.get(username=req.user.username)
    user_profile=profile.objects.get(user=user_object)
    return render(req,"index.html",{"posts":post_list,"Category":Category_list,"user_profile":user_profile})
@login_required(login_url="login")
def delete_post(req,pk):
    user=User.objects.get(username=req.user.username)
    post_object=Post.objects.filter(id=pk).first()
    if(post_object.get_name().capitalize()==user.username.capitalize()):
        post_object.delete()
    return redirect("/")
@login_required(login_url="login")
def chatpage(req,pk):
    username=req.GET.get("username")
    post_details=Post.objects.get(id=pk)
    return render(req,"chat_page.html",{"username":username,"pk":pk,"post_details":post_details})
@login_required(login_url="login")
def send(req):
    message=req.POST["message"]
    username=req.POST["username"]
    post_id=req.POST["post_id"]
    date=calc_time()
    new_message=Message.objects.create(message=message,user=username,post_id=post_id,date=date)
    new_message.save()
    return HttpResponse("message sent succesfully")
@login_required(login_url="login")
def getMessages(req,pk):
    post_details=Post.objects.get(id=pk)
    rest=Message.objects.filter(post_id=post_details.id)
    return JsonResponse({"rest":list(rest.values())})










