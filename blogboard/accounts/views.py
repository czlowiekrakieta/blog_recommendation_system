from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from recommendations.models import RecommendationBlog, RecommendationUser
from .forms import UserLoginForm
# Create your views here.
from blogs.models import UserFollowings, Rating
from .forms import UserLikesForm, UserRegisterForm, UserLoginForm, UserLogoutForm
import os
from comments.models import Comment
# from recommendations.models import ManageCalculations

templates_location = os.path.join(os.path.dirname(os.path.dirname(__file__)).rstrip("/blogs"), "templates")
def merge_timestamp(ratings, comments):
    show_list = []
    i, j = 0, 0
    while i < len(ratings) and j < len(comments):
        if ratings[i].timestamp < comments[j].timestamp:
            show_list.append(comments[j])
            j += 1
        else:
            show_list.append(ratings[i])
            i += 1

    if i == len(ratings):
        show_list += comments[j:]
    else:
        show_list += ratings[i:]

    return show_list

def user_follow(request, pk=None):
    instance = get_object_or_404(User, id=pk)
    user = get_object_or_404(UserFollowings, user=request.user)

    user.following.add(instance)
    user.save()

    # context_data = {
    #     "object": instance,
    #     "ratings": instance.rating_set.all(),
    #     "followers": UserFollowings.objects.filter(following=pk),
    # }

    return redirect("/users/" + str(pk))


def user_unfollow(request, pk=None):
    instance = get_object_or_404(User, id=pk)
    user = get_object_or_404(UserFollowings, user=request.user)

    user.following.remove(instance)
    user.save()

    # context_data = {
    #     "object": instance,
    #     "ratings": instance.rating_set.all(),
    #     "followers": UserFollowings.objects.filter(following=pk),
    # }

    return redirect("/users/" + str(pk))

def login_view(request):

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        path = form.cleaned_data.get("path")

        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect(path)

    path = form.cleaned_data['path']

    return redirect(path)
    #return render(request, templates_location+"/account_gate.html", {"form":form})


def logout_view(request):
    form = UserLogoutForm(request.POST or None)
    #print(form)
    if form.is_valid():
        path = form.cleaned_data.get("path")

        logout(request)
        return redirect(path)

    path = form.cleaned_data['path']
    return redirect(path)


def register_page(request):

    user_form = UserRegisterForm(request.POST or None)
    user_likes = UserLikesForm(request.POST or None)
    if user_form.is_valid() and user_likes.is_valid():
        user = user_form.save(commit=False)
        pwd = user_form.cleaned_data.get("password")
        user.set_password(pwd)
        user.save()

        user_foll = user_likes.save(commit=False)
        user_foll.set_user(user)
        user_foll.save()
        
        c = RecommendationUser(user=user_foll)
        c.save()
        
        login(request, user)
        return redirect('main')

    context = {
        "user_form":user_form,
        "user_likes":user_likes
    }

    return render(request, "register.html", context)

def user_detail(request, pk=None):
    login_form = UserLoginForm(request.POST or None)
    logout_form = UserLogoutForm(request.POST or None)
    path = request.path

    login_form.set_path(path)
    logout_form.set_path(path)

    a_user = get_object_or_404(User, id=pk)
    instance = get_object_or_404(UserFollowings, user=a_user)

    ratings = list(Rating.objects.filter(user=a_user).order_by("-timestamp"))
    comments = list(Comment.objects.filter(user=a_user).order_by("-timestamp"))

    show_list = merge_timestamp(ratings, comments)


    context_data = {
        "user_iq": a_user,
        "followingblogs": instance.followed_blogs.all(),
        "followingusers": instance.following.all(),
        "followers": UserFollowings.objects.filter(following=a_user.id),
        "show_list":show_list,
    }

    if request.user.is_authenticated():
        print(request.user.id, a_user.id)
        context_data['logged'] = True
        context_data['logout_form'] = logout_form
        context_data['current_user'] = UserFollowings.objects.get(user=request.user)
    else:
        context_data['login_form'] = login_form

    return render(request, templates_location+"/userfollowings_detail.html", context_data)


