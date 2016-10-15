from django.db import models
from blogs.models import Blog, Rating, UserFollowings, fields
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import numpy as np
from .math import most_popular, most_popular_category, create_user_matrix, create_blog_matrix, create_corr_matrix, similar

# Create your models here.
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


class ManageCalculations(models.Model):
    last_eval = models.DateTimeField(default=pytz.UTC.localize(timezone.datetime(2010, 1, 1)))
    last_regression = models.DateTimeField(default=pytz.UTC.localize(timezone.datetime(2010, 1, 1)))

    def was_evaluated_recently(self):
        if timezone.now() - timezone.timedelta(days=7) > self.last_eval:
            self.last_eval = timezone.now()
            self.save()
            return False
        else:
            return True

    def was_regressed_recently(self):
        if timezone.now() - timezone.timedelta(days=7) > self.last_regression:
            self.last_regression = timezone.now()
            self.save()
            return False
        else:
            return True

    def calc_users(self):
        users = UserFollowings.objects.all()
        m, d = create_user_matrix()
        corr, id_list = create_corr_matrix(m)
        for usf in users:
            real_user = usf.user
            sim = similar(real_user.id, corr, id_list, d, 'users')
            r = RecommendationUser.objects.get(user=usf)
            if r.similar.all().count():
                r.similar.remove(*r.similar.all())
            r.similar.add(*sim)

    def calc_blogs(self):
        blogs = Blog.objects.all()
        m, d = create_blog_matrix()
        corr, id_list = create_corr_matrix(m)
        for bl in blogs:
            sim = similar(bl.id, corr, id_list, d, 'blogs')
            r = RecommendationBlog.objects.get(blog=bl)
            if r.similar.all().count():
                r.similar.remove(*r.similar.all())
            r.similar.add(*sim)

    def regression(self, what, user=None, blog=None):
        ratings = Rating.objects.none()
        obj = 1
        if what == 'user':
            obj = UserFollowings.objects.get(user=user)
            ratings = Rating.objects.filter(user=user)
        elif what == 'blog':
            obj = Blog.objects.get(blog=blog)
            ratings = Rating.objects.filter(blog=blog)

        z = ratings.count()
        if not z:
            return
        inputs = np.zeros((z, len(fields)-1))
        values = np.zeros(z)
        weights = obj.get_fields_arr()

        for i, rat in enumerate(ratings):
            arr = rat.get_fields_arr()
            inputs[i, :] = arr[1:]
            values[i] = arr[0]

        model = LinearRegression(X=inputs, Y=values, weights=weights)
        model.fit(with_cost_history=False)
        weights = model.get_params()
        obj.set_fields_from_arr(weights)


    def user_regression(self):
        users = User.objects.all()
        for us in users:
            self.regression(what='user', user=us)



class RecommendationUser(models.Model):
    user = models.OneToOneField(UserFollowings)
    similar = models.ManyToManyField(User, related_name='similar')


class RecommendationBlog(models.Model):
    blog = models.OneToOneField(Blog)
    #vector = ArrayField(models.FloatField(null=True, blank=True), len(fields)-1, null=True)
    similar = models.ManyToManyField(Blog, related_name='similar')


class MostPopularByCat(models.Model):
    category = models.CharField(max_length=30)
    last_eval = models.DateTimeField(default=pytz.UTC.localize(timezone.datetime(2010, 1, 1)))
    blogs = models.ManyToManyField(Blog, related_name='pop_blogs')

    def __str__(self):
        return self.category

    def was_evaluated_recently(self):
        if timezone.now() - timezone.timedelta(days=7) > self.last_eval:
            return False
        else:
            return True

    def evaluate(self):
        if self.category == 'general_ratings':
            things = most_popular()
        else:
            things = most_popular_category(category=self.category)
        if self.blogs.all().count():
            self.blogs.remove(*self.blogs.all())
        self.blogs.add(*things)
