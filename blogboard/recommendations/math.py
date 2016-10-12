import numpy as np
from django.db.models import Count
from django.utils import timezone
from blogs.models import Blog, Rating, UserFollowings, fields
from django.contrib.auth.models import User

last_time_run = 0 #we will run these things periodically, so there is need for variable storing last time we did this

#turn all of this into class
def create_user_matrix():
    users = User.objects.all()
    matrix = np.zeros( ( users.count(), len(fields) ) )
    d = {}
    for i, user in enumerate(users):
        rat = Rating.objects.filter(user=user)
        features = np.array(rat.values_list(*fields[1:]))
        ratings = np.array(rat.values_list('general_ratings')) - 1
        try:
            matrix[i, ] = np.hstack((user.id, np.mean(features*ratings, axis=0) ) )
        except ValueError:
            matrix[i, ] = np.hstack((user.id, np.zeros(len(fields)-1)))
        d[user.id] = i
    return matrix, d

def create_blog_matrix():
    blogs = Blog.objects.all()
    matrix = np.zeros((blogs.count(), len(fields)))
    d = {}
    for i, blog in enumerate(blogs):
        blog.create_coefficients()
        matrix[i, ] = np.hstack( (blog.id, np.asarray([getattr(blog, x) for x in fields[1:]])) )
        d[blog.id] = i
    return matrix, d

def followed_users_liked(userfollowings):
    followed_users = userfollowings.following.all()
    blogs_qs = Rating.objects.none()
    for user in followed_users:
        ratings = Rating.objects.filter(user=user, general_ratings=2)
        blogs_qs = blogs_qs | ratings

    blogs_qs = blogs_qs.order_by('-timestamp')[:10]
    bl = list(set([x.blog.id for x in blogs_qs]))
    return Blog.objects.filter(id__in = bl)

def create_corr_matrix(blog_matrix):
    return np.corrcoef(blog_matrix[:, 1:]), blog_matrix[:, 0]

def similar(id, corr_matrix, id_list, dictionary, what):
    nr = dictionary[id]
    r_sorted = np.argsort(corr_matrix[nr, :])[::-1][1:]
    ids = np.asarray(id_list)[r_sorted]

    if what=='blogs':
        return Blog.objects.filter(id__in = ids)
    if what=='users':
        return User.objects.filter(id__in = ids)

def users_who_liked_also_liked():
    pass

def run_regression_for_users():
    pass

def run_regression_for_blogs():
    pass

def predict_ratings():
    pass

def calculate_temporal_ratings(set_of_ratings):
    # s = set_of_ratings.values('general_ratings').annotate(rating=Count('general_ratings'))
    d = set()
    for rat in set_of_ratings:

        if rat.blog.id not in d:
            d = d | set([rat.blog.id])
    l = []
    for id in d:
        s = set_of_ratings.filter(blog__id=id).values('general_ratings').annotate(rating=Count('general_ratings'))
        s = {x['general_ratings']:x['rating'] for x in s}
        for i in range(3):
            if i not in s:
                s[i] = 0
        z = sum(s.values())
        l.append([id, sum([x*s[x]/z for x in range(3)] )])

    return np.asarray(l)


def most_popular():
    t = timezone.now()

    rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=1), t))
    ar = calculate_temporal_ratings(rat)
    order = np.argsort(ar[:, 1], axis=0)[::-1]

    return Blog.objects.filter(id__in=ar[:, 0][order])

def most_popular_category(category):
    t = timezone.now()

    rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=1), t))

    ar = calculate_temporal_ratings(rat)
    blog_list = Blog.objects.none()
    for bl_id in ar[:, 0]:
        ob = Blog.objects.filter(id=bl_id)
        bl = getattr(ob[0], category)
        if bl > 2:
            blog_list = blog_list | ob

    return blog_list











