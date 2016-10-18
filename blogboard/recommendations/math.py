import numpy as np
from django.db.models import Count
from django.utils import timezone
from blogs.models import Blog, Rating, UserFollowings, fields
from django.contrib.auth.models import User


#turn all of this into class
class LinearRegression:
    def __init__(self, X, Y, weights):

        self.N = X.shape[0]
        self.X = X
        self.Y = Y

        self.weights = np.array(weights)
        self.cost_history = []

    def fit(self, iterations=int(1e3), alpha=1e-3, reg=1e-3, with_cost_history=True):
        self.reg = reg
        while iterations:
            iterations -= 1

            residuals = np.dot(self.X, self.weights) - self.Y.T

            derivatives = np.asarray(list(map(lambda i: np.mean(residuals * self.X[:, i]), range(self.X.shape[1]))))
            part1 = alpha*derivatives
            part2 = self.reg*self.weights
            self.weights -= alpha * derivatives + self.reg * self.weights
            if with_cost_history:
                cost = np.mean(residuals * residuals)
                self.cost_history.append(cost)

    def predict(self, tab):
        self.pred = np.dot(np.concatenate([np.repeat(1, tab.shape[0])[None].T, tab], axis=1), self.weights)
        return self.pred

    def get_cost_history(self):
        return self.cost_history

    def get_params(self):
        return self.weights



# def create_user_matrix():
#     users = User.objects.all()
#     matrix = np.zeros( ( users.count(), len(fields) ) )
#     d = {}
#     for i, user in enumerate(users):
#         rat = Rating.objects.filter(user=user)
#         features = np.array(rat.values_list(*fields[1:]))
#         ratings = np.array(rat.values_list('general_ratings')) - 1
#         try:
#             matrix[i, ] = np.hstack((user.id, np.mean(features*ratings, axis=0) ) )
#         except ValueError:
#             matrix[i, ] = np.hstack((user.id, np.zeros(len(fields)-1)))
#         d[user.id] = i
#     return matrix, d
#
# def create_blog_matrix():
#     blogs = Blog.objects.all()
#     matrix = np.zeros((blogs.count(), len(fields)))
#     d = {}
#     for i, blog in enumerate(blogs):
#         blog.create_coefficients()
#         matrix[i, ] = np.hstack( (blog.id, np.asarray( blog.get_fields_arr() )) )
#         d[blog.id] = i
#     return matrix, d
#
# def followed_users_liked(userfollowings):
#     followed_users = userfollowings.following.all()
#     blogs_qs = Rating.objects.none()
#     for user in followed_users:
#         ratings = Rating.objects.filter(user=user, general_ratings=2)
#         blogs_qs = blogs_qs | ratings
#
#     blogs_qs = blogs_qs.order_by('-timestamp')[:10]
#     bl = list(set([x.blog.id for x in blogs_qs]))
#     return Blog.objects.filter(id__in = bl)
#
# def create_corr_matrix(blog_matrix):
#     return np.corrcoef(blog_matrix[:, 1:]), blog_matrix[:, 0]
#
# def similar(id, corr_matrix, id_list, dictionary, what):
#     nr = dictionary[id]
#     r_sorted = np.argsort(corr_matrix[nr, :])[::-1][1:]
#     ids = np.asarray(id_list)[r_sorted]
#
#     if what=='blogs':
#         return Blog.objects.filter(id__in = ids)
#     if what=='users':
#         return User.objects.filter(id__in = ids)
#
# def users_who_liked_also_liked():
#     pass
#
# def predict_ratings():
#     pass
#
# def calculate_temporal_ratings(set_of_ratings):
#     # s = set_of_ratings.values('general_ratings').annotate(rating=Count('general_ratings'))
#     d = set()
#     for rat in set_of_ratings:
#
#         if rat.blog.id not in d:
#             d = d | set([rat.blog.id])
#     l = []
#     for id in d:
#         s = set_of_ratings.filter(blog__id=id).values('general_ratings').annotate(rating=Count('general_ratings'))
#         s = {x['general_ratings']:x['rating'] for x in s}
#         for i in range(3):
#             if i not in s:
#                 s[i] = 0
#         z = sum(s.values())
#         l.append([id, sum([x*s[x]/z for x in range(3)] )])
#
#     return np.asarray(l)
#
#
# def most_popular():
#     t = timezone.now()
#
#     rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=10), t))
#     ar = calculate_temporal_ratings(rat)
#     print(ar)
#     order = np.argsort(ar[:, 1], axis=0)[::-1]
#
#     return Blog.objects.filter(id__in=ar[:, 0][order])
#
# def most_popular_category(category):
#     t = timezone.now()
#
#     rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=10), t))
#
#     ar = calculate_temporal_ratings(rat)
#     blog_list = Blog.objects.none()
#     for bl_id in ar[:, 0]:
#         ob = Blog.objects.filter(id=bl_id)
#         bl = getattr(ob[0], category)
#         if bl > 2:
#             blog_list = blog_list | ob
#
#     return blog_list
#
#
# def calc_users():
#     print("its happening")
#     users = UserFollowings.objects.all()
#     m, d = create_user_matrix()
#     corr, id_list = create_corr_matrix(m)
#     for usf in users:
#         real_user = usf.user
#         sim = similar(real_user.id, corr, id_list, d, 'users')
#         r = RecommendationUser.objects.get(user=usf)
#         if r.similar.all().count():
#             r.similar.remove(*r.similar.all())
#         r.similar.add(*sim)
#
#
# def calc_blogs():
#     print("its happening")
#     blogs = Blog.objects.all()
#     m, d = create_blog_matrix()
#     corr, id_list = create_corr_matrix(m)
#     for bl in blogs:
#         sim = similar(bl.id, corr, id_list, d, 'blogs')
#         r = RecommendationBlog.objects.get(blog=bl)
#         if r.similar.all().count():
#             r.similar.remove(*r.similar.all())
#         r.similar.add(*sim)
#
#
# def regression( what, user=None, blog=None):
#     ratings = Rating.objects.none()
#     obj = 1
#     if what == 'user':
#         obj = UserFollowings.objects.get(user=user)
#         ratings = Rating.objects.filter(user=user)
#     elif what == 'blog':
#         obj = Blog.objects.get(blog=blog)
#         ratings = Rating.objects.filter(blog=blog)
#
#     z = ratings.count()
#     if not z:
#         return
#     inputs = np.zeros((z, len(fields) - 1))
#     values = np.zeros(z)
#     weights = obj.get_fields_arr()
#
#     for i, rat in enumerate(ratings):
#         arr = rat.get_fields_arr()
#         inputs[i, :] = arr[1:]
#         values[i] = arr[0]
#
#     model = LinearRegression(X=inputs, Y=values, weights=weights)
#     model.fit(with_cost_history=False)
#     weights = model.get_params()
#     obj.set_fields_from_arr(weights)
#
#
# def user_regression():
#     users = User.objects.all()
#     for us in users:
#         self.regression(what='user', user=us)
#
#








