from django.conf.urls import url
from django.contrib import admin
from accounts.views import login_view, logout_view, register_page, user_detail, user_follow, user_unfollow

urlpatterns = [
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_page, name='register'),
    url(r'^(?P<pk>\d+)/$', user_detail, name='user-detail'),
    url(r'^(?P<pk>\d+)/follow', user_follow, name='user-follow'),
    url(r'^(?P<pk>\d+)/unfollow', user_unfollow, name='user-unfollow'),

    ]