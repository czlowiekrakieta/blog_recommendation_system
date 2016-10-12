from django.shortcuts import render, get_object_or_404, redirect
from blogs.models import Blog, UserFollowings, Rating
import os
from django.db.models import Count
from .forms import RatingForm, NewBlogForm
from recommendations import math
from recommendations.models import ManageCalculations, RecommendationBlog, RecommendationUser, MostPopularByCat
from comments.forms import CommentForm, VoteForm
from accounts.forms import UserLoginForm, UserLogoutForm
from blogs.models import fields, Rating
from comments.models import Comment
from accounts.views import merge_timestamp
from django.db.models import Count
from time import time
from blogboard.common import blog_and_user
templates_location = os.path.join(os.path.dirname(os.path.dirname(__file__)).rstrip("/blogs"), "templates")



def blog_detail(request, pk=None):

    current_user, instance = blog_and_user(request, pk=pk)

    rate_form = RatingForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    voteform = VoteForm(request.POST or None)
    login_form = UserLoginForm(request.POST or None)
    logout_form = UserLogoutForm(request.POST or None)
    path = request.path

    login_form.set_path(path)
    logout_form.set_path(path)
    comment_form.set_path(path)
    voteform.set_path(path)
    s = time()
    countings = list(map(lambda x: Rating.objects.filter(blog=instance).values(x).annotate(Count(x)), fields))
    s = time()
    maximum = 0
    def turn_to_dict(nr):
        d = {countings[nr][i][fields[nr]]:countings[nr][i][fields[nr]+"__count"] for i in range(len(countings[nr]))}
        for i in range(5):
            if i not in d:
                d[i] = 0
        final = [d[i] for i in range(5)]
        return final
    countings = dict(zip(fields, list(map(turn_to_dict, range(len(fields))))))
    for f in fields:
        maximum = max( maximum, max(countings[f]))

    g_rating = countings.pop("general_ratings")

    mc = get_object_or_404(ManageCalculations, pk=1)
    if not mc.was_evaluated_recently():
        mc.calc_blogs()
        mc.calc_users()

    sim = RecommendationBlog.objects.get(blog=instance)
    similar = sim.similar.all()

    comments = instance.comment_set.all()
    print(comments)
    context_data = {
        "rate_form": rate_form,
        "voteform": voteform,
        "blog": instance,
        "ratings": instance.rating_set.all(),
        "followers": instance.userfollowings_set.all(),
        "comments": comments[:10],
        "comment_form": comment_form,
        'logged': False,
        'current_url': path,
        'countings': countings,
        'g_rating':g_rating[:-2],
        'similar': similar,
        'maximum': maximum
    }


    if current_user.is_authenticated:
        context_data['logged'] = True
        context_data['current_user'] = current_user
        context_data['logged_user'] = UserFollowings.objects.get(user=current_user)
        context_data['logout_form'] = logout_form
        if Rating.objects.filter(user=current_user, blog=instance).exists():
            context_data['user_rate'] = Rating.objects.get(user=current_user, blog=instance)

    else:
        context_data['login_form'] = login_form

    return render(request, templates_location+"/blog_detail.html", context_data)

def blog_rate(request, pk=None):
    current_user, instance = blog_and_user(request, pk=pk)

    rate_form = RatingForm(request.POST or None)


    if rate_form.is_valid():
        new_rating = rate_form.save(commit=False)
        new_rating.set_fks(user=current_user, blog=instance)

        if Rating.objects.filter(user=current_user, blog=instance).exists():
            former_rating = Rating.objects.get(user=current_user, blog=instance)
            former_rating.delete()

        new_rating.save()
    return redirect("/blog/" + str(pk))

def blog_comment(request, pk=None):
    current_user, instance = blog_and_user(request, pk=pk)

    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.set_fks(user=current_user, blog=instance)
        new_comment.save()

    return redirect("/blog/" + str(pk))


def blog_follow(request, pk=None):
    user = get_object_or_404(UserFollowings, user=request.user)
    instance = get_object_or_404(Blog, id=pk)

    user.followed_blogs.add(instance)
    user.save()

    # context_data = {
    #     "object": instance,
    #     "ratings": instance.rating_set.all(),
    #     "followers": instance.userfollowings_set.all(),
    # }

    return redirect("/blog/" + str(pk))

def blog_unfollow(request, pk=None):
    user = get_object_or_404(UserFollowings, user=request.user)
    instance = get_object_or_404(Blog, id=pk)

    user.followed_blogs.remove(instance)
    user.save()

    # context_data = {
    #     "object": instance,
    #     "ratings": instance.rating_set.all(),
    #     "followers": instance.userfollowings_set.all(),
    # }


    return redirect("/blog/" + str(pk))



def main_page(request):
    login_form = UserLoginForm(request.POST or None)
    logout_form = UserLogoutForm(request.POST or None)
    path = request.path

    login_form.set_path(path)
    logout_form.set_path(path)

    if request.user.is_authenticated:
        user = request.user
        instance = get_object_or_404(UserFollowings, user=user)

        followed_users = instance.following.all()
        followed_blogs = instance.followed_blogs.all()

        ratings = Rating.objects.none()
        comments = Comment.objects.none()

        for user in followed_users:
            ratings = ratings | Rating.objects.filter(user=user)
            comments = comments | Comment.objects.filter(user=user)

        ratings = ratings.order_by("-timestamp")
        comments = comments.order_by("-timestamp")
        show_list = merge_timestamp(ratings, comments)

        foll_likes = math.followed_users_liked(instance)

        context_data = {
            'logged': True,
            "user_iq": instance,
            "blogs_iq": followed_blogs,#.order_by("-general_ratings"),
            "followingusers": followed_users,
            'logout_form': logout_form,
            'show_list': show_list,
            'foll_likes':foll_likes
        }

    else:
        context_data = {
            'login_form': login_form
        }

    # popular = math.most_popular()
    # if len(popular) > 5:
    #     popular = popular[:5]
    #
    # context_data['popular'] = popular
    # dict_categories_popularity = {}
    # for f in fields:
    #     dict_categories_popularity[f] = math.most_popular_category(f)
    #     if len(dict_categories_popularity[f]) > 5:
    #         dict_categories_popularity[f] = dict_categories_popularity[f][:5]
    #
    #
    # context_data['cat_popularity'] = dict_categories_popularity

    s = []
    for f in fields:
        mp = MostPopularByCat.objects.get(category=f)
        if not mp.was_evaluated_recently():
            mp.evaluate()
        s.append(mp.blogs.all())

    context_data['popular'] = s[0]
    dict_pop = dict(zip(fields[1:], s[1:]))
    context_data['cat_popularity'] = dict_pop


    return render(request, templates_location+"/main.html", context_data)


def register_blog(request):
    if request.user.is_staff:
        newblog = NewBlogForm(request.POST or None)
        context_data = {
            "newblog":newblog
        }

        if newblog.is_valid():
            blog = newblog.save(commit=False)
            import_data = {x:int(newblog.cleaned_data[x]) for x in fields[1:]}
            blog.save()

            blog.set_start_values(import_data)

            return redirect("/blog/add")

        return render(request, templates_location+"/register_blog.html", context_data)
    else:
        return redirect('main')



