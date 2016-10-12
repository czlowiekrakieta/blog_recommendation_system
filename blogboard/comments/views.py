from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Vote
from .forms import CommentForm, VoteForm
from blogs.models import Blog
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
templates_location = os.path.join(os.path.dirname(os.path.dirname(__file__)).rstrip("/blogs"), "templates")
# Create your views here.
def comment_reply(request, pk=None):
    pass

def comment_post(request, pk=None):
    current_user, instance = blog_and_user(request, pk=pk)

    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.set_fks(user=current_user, blog=instance)
        new_comment.save()

def comment_vote(request, pk=None):
    comment = get_object_or_404(Comment, pk=pk)

    voteform = VoteForm(request.POST or None)

    if voteform.is_valid():
        new_vote = voteform.save(commit=False)
        us = request.user
        new_vote.set_fks(us, comment)

        if Vote.objects.filter(user=us, comment=comment).exists():
            former_vote = Vote.objects.get(user=us, comment=comment)
            former_vote.delete()

        new_vote.save()

    return redirect("/blog/" + str(comment.blog.id))

def comment_page(request, pk=None):
    blog = get_object_or_404(Blog, pk=pk)
    qs = blog.comment_set.all().order_by('binom')

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
        "comments":comments
    }
    return render(request, templates_location+"/comments.html", context_data)