from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Vote
from .forms import CommentForm, VoteForm
from blogs.models import Blog
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blogboard.common import blog_and_user
templates_location = os.path.join(os.path.dirname(os.path.dirname(__file__)).rstrip("/blogs"), "templates")
# Create your views here.
def comment_reply(request, pk=None):
    pass

def comment_post(request, pk=None):
    current_user, instance = blog_and_user(request, pk=pk)

    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        path = comment_form.cleaned_data.get("path")
        new_comment.set_fks(user=current_user, blog=instance)
        new_comment.save()

        return redirect(path)

    return redirect(comment_form.cleaned_data['path'])

def comment_vote(request, pk=None):
    comment = get_object_or_404(Comment, pk=pk)
    voteform = VoteForm(request.POST or None)
    us = request.user

    if Vote.objects.filter(user=us, comment=comment).exists():
        former_vote = Vote.objects.get(user=us, comment=comment)
        former_vote.delete()

    if voteform.is_valid():
        new_vote = voteform.save(commit=False)

        path = voteform.cleaned_data.get("path")
        new_vote.set_fks(us, comment)
        new_vote.save()
        comment.set_binom()
        return redirect(path)

    return redirect(voteform.cleaned_data['path'])

def comment_page(request, pk=None):
    blog = get_object_or_404(Blog, pk=pk)
    qs = blog.comment_set.all().order_by('binom')
    path = request.path
    voteform = VoteForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    comment_form.set_path(path)
    voteform.set_path(path)

    paginator = Paginator(qs, 10)
    comment = request.GET.get('comment')
    try:
        comments = paginator.page(comment)
    except PageNotAnInteger:
        comments = paginator.page(1)

    except EmptyPage:
        comments = paginator.comment(paginator.num_pages)

    context_data = {
        "blog":blog,
        "comments":comments,
        "voteform":voteform,
        "comment_form":comment_form
    }
    return render(request, templates_location+"/comments.html", context_data)