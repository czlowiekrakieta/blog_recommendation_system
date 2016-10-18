from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
import numpy as np

# Create your models here.
languages = [x for x in enumerate(['english', 'polish', 'german', 'french', 'russian'])]
rates = [x for x in enumerate(['not at all', 'a bit', 'evenly with other topics', 'dominates others', \
                               'speaks only about it'])]
likes = [x for x in enumerate(['not at all', 'not so much', 'do not care', 'a bit', 'a lot'])]
fields = ['general_ratings', 'politics', 'sports', 'culture', 'tech', 'travel', 'fashion', 'hard_science', 'soft_science']

class Blog(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    language = models.IntegerField(default=0, choices=languages)
    general_ratings = models.FloatField(null=True)
    politics = models.FloatField(null=True)
    sports = models.FloatField(null=True)
    culture = models.FloatField(null=True)
    tech = models.FloatField(null=True)
    travel = models.FloatField(null=True)
    fashion = models.FloatField(null=True)
    hard_science = models.FloatField(null=True)
    soft_science = models.FloatField(null=True)

    coefficients = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name + " by " +  self.author

    def set_coefficients_by_name(self): #this is to be rewritten to acknowledge fact that we possess some information already
        countings = list(map(lambda x: Rating.objects.filter(blog=self).values(x).annotate(Count(x)), fields))

        def turn_to_dict(nr):
            d = {countings[nr][i][fields[nr]]: countings[nr][i][fields[nr] + "__count"] for i in
                 range(len(countings[nr]))}
            for i in range(5):
                if i not in d:
                    d[i] = 0
            final = [d[i] for i in range(5)]
            return final

        countings = dict(zip(fields, list(map(turn_to_dict, range(len(fields))))))
        print(countings)
        for key, value in countings.items():
            if key == 'general_ratings':
                s = sum(value)
                coef = sum([x*value[x]/s for x in range(3)])

            else:
                s = sum(value)
                coef = sum([x*value[x]/s for x in range(5)])


            setattr(self, key, coef)
            self.save()

    def generate_coefficients(self):
        x = np.round(np.random.randn(3,9)/10, 3)
        s = ''.join(list(map(lambda x: str(x)+";", np.ravel(x) )))
        setattr(self, 'coefficients', s[:-1])
        self.save()

    def retrieve_coefficients(self):
        return np.reshape(np.asarray(list(map(float, getattr(self, 'coefficients').split(";") ))), (3,9) )

    def set_coefficients(self, array):
        s = ''.join(list(map(lambda x: str(x)+";", np.ravel(x))))
        setattr(self, 'coefficients', s[:-1])
        self.save()

    def get_fields_arr(self):
        z = self.__dict__
        return [z[f] for f in fields[1:]]


    def set_fields_from_arr(self, arr):
        for i, f in enumerate(fields[1:]):
            setattr(self, f, arr[i])

        self.save()

class Rating(models.Model):
    user = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    general_ratings = models.IntegerField(default=None, choices=[x for x in enumerate(['bad', 'meh', 'good'])])
    politics = models.IntegerField(default=None, choices=rates)
    sports = models.IntegerField(default=None, choices=rates)
    culture = models.IntegerField(default=None, choices=rates)
    tech = models.IntegerField(default=None, choices=rates)
    travel = models.IntegerField(default=None, choices=rates)
    fashion = models.IntegerField(default=None, choices=rates)
    hard_science = models.IntegerField(default=None, choices=rates)
    soft_science = models.IntegerField(default=None, choices=rates)

    def set_fks(self, user, blog):
        self.user = user
        self.blog = blog

    def class_str(self):
        return 'rating'

    def get_fields_arr(self):
        z = self.__dict__
        return [z[f] for f in fields]

class UserFollowings(models.Model):
    user = models.OneToOneField(User)
    followed_blogs = models.ManyToManyField(Blog, blank=True, null=True)
    following = models.ManyToManyField(User, related_name='User', blank=True, null=True)

    politics = models.FloatField(default=2)
    sports = models.FloatField(default=2)
    culture = models.FloatField(default=2)
    tech = models.FloatField(default=2)
    travel = models.FloatField(default=2)
    fashion = models.FloatField(default=2)
    hard_science = models.FloatField(default=2)
    soft_science = models.FloatField(default=2)


    def __str__(self):
        return self.user.username


    def set_user(self, user_object):
        self.user = user_object

    def class_str(self):
        return 'userfollowings'

    def get_fields_arr(self):
        z = self.__dict__
        return np.asarray([z[f] for f in fields[1:]])

    def set_fields_from_arr(self, arr):
        for i, f in enumerate(fields[1:]):
            setattr(self, f, arr[i])

        self.save()


