"""jango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib import admin

django.setup()

# import settings
# settings.configure()
from  app import views as app_views
from django.contrib.auth import views as auth_views



urlpatterns = [

    url(r'^$',app_views.index,name='theindex'),
    url(r'^admin/', admin.site.urls),
    url(r'^artists/create$',app_views.createartist,name='artistscreate'),
    url(r'^artists$',app_views.artists,name='artists'),
    url(r'^artists/(?P<id>\d+)$',app_views.artistdetails,name='artistdetails'),
    url(r'^course/create$',app_views.createcourse,name='coursecreate'),
    url(r'^courses$',app_views.courses,name='courses'),
    url(r'^courses/(?P<id>\d+)$',app_views.coursedetails,name='coursedetails'),
    url(r'^student/create$',app_views.createstudent,name='studentcreate'),
    url(r'^students$',app_views.students,name='students'),
    url(r'^studentprofile$',app_views.studentprofile,name='studentprofile'),
    url(r'^studentdetails$', app_views.studentdetails, name='studentdetails'),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'loginout.html'}, name='logout'),
    url(r'^register/$', app_views.register, name='register'),
]
