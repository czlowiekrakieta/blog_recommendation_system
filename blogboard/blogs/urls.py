from django.conf.urls import url
from django.contrib import admin
from blogs.views import blog_detail, blog_follow, blog_unfollow, blog_rate, blog_comment, register_blog, blog_search_list, blog_adv_search_list
#from blogs.views import BlogDetailView

urlpatterns = [
    url(r'^add/$', register_blog, name='register-blog'),
    url(r'^(?P<pk>\d+)/$', blog_detail, name='blog-detail'),
    url(r'^(?P<pk>\d+)/follow', blog_follow, name='blog-follow'),
    url(r'^(?P<pk>\d+)/unfollow', blog_unfollow, name='blog-unfollow'),
    url(r'^(?P<pk>\d+)/rate', blog_rate, name='blog-rate'),
    url(r'^(?P<pk>\d+)/comment', blog_comment, name='blog-comment'),
    url(r'^search/', blog_search_list, name='blog-search'),
    url(r'^advsearch/', blog_adv_search_list, name='blog-adv-search')
]
