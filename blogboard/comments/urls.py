from django.conf.urls import url
from comments.views import comment_vote, comment_page

urlpatterns = [
    url(r'^vote/(?P<pk>\d+)/$', comment_vote, name='comment-vote'),
    url(r'^view/(?P<pk>\d+)/$', comment_page, name='view-all')
]