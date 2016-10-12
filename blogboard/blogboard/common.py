from django.shortcuts import get_object_or_404
from blogs.models import Blog


def blog_and_user(request, pk=None):
    return request.user, get_object_or_404(Blog, id=pk)