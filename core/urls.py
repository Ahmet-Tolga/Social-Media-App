"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sciencer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login",views.login_page,name="login"),
    path("logout",views.logout,name="logout"),
    path("settings",views.settings,name="settings"),
    path("upload",views.upload,name="upload"),
    path("like-post",views.like_post,name="like-post"),
    path("profile/<str:pk>",views.profile_page,name="profile"),
    path("follow",views.follow,name="follow"),
    path("category/<str:pk>",views.show,name="show"),
    path("delete/<str:pk>",views.delete_post,name="delete_post"),
    path("send/message",views.send),
    path("getmessages/<str:pk>/",views.getMessages),
    path("chatpage/<str:pk>",views.chatpage,name="chatpage"),
    path("profile/chatpage/<str:pk>",views.chatpage,name="chatpage"),

]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
