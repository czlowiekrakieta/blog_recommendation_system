from django.db import models
from blogs.models import Blog, Rating, UserFollowings, fields
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import numpy as np
from .math import most_popular, most_popular_category, create_user_matrix, create_blog_matrix, create_corr_matrix, similar

# Create your models here.
class ManageCalculations(models.Model):
    last_eval = models.DateTimeField(default=pytz.UTC.localize(timezone.datetime(2010, 1, 1)))

    def was_evaluated_recently(self):
        if timezone.now() - timezone.timedelta(days=7) > self.last_eval:
            self.last_eval = timezone.now()
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
