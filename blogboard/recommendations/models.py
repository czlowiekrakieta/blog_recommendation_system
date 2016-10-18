from django.db import models
from django.db.models import Count
from blogs.models import Blog, Rating, UserFollowings, fields
from django.contrib.auth.models import User
from django.utils import timezone
from blogboard.common import threshold
import pytz
import numpy as np

class Calculations:
    def __init__(self):
        self.users = User.objects.all()
        c = 0
        self.user_dict = {}
        for us in self.users:
            if len(us.rating_set.all()) > threshold:
                self.user_dict[c] = us.id
                c += 1
                rat = Rating.objects.filter(user=us)
                features = np.array(rat.values_list(*fields[1:]))
                ratings = np.array(rat.values_list('general_ratings')) - 1
                us.set_fields_from_arr( np.mean(features * ratings, axis=0) )
            else:
                self.users.remove(us)
        self.user_rating_matrix = np.zeros((c,c))
        self.user_coef_matrix = np.zeros((c,c))
        self.b = 0
        self.blogs = Blog.objects.all()
        self.blog_dict = {}
        for bl in self.blogs:
            if len(bl.rating_set.all()) > threshold:
                self.blog_dict[b] = bl.id
                self.b += 1
            else:
                self.blogs.remove(bl)
        self.blog_matrix = np.zeros((self.b,self.b))
        self.liking_matrix = np.zeros((self.b,self.b))

    def calc_user_matrices(self):
        for i, us in enumerate(self.users):
            r = Rating.objects.filter(user=us)
            usf = UserFollowings.objects.get(user=us)
            for j, inner_us in enumerate(self.users[i+1:]):

                usf_inner = UserFollowings.objects.get(user=inner_us)
                inner_r = Rating.objects.filter(user=inner_us)
                blogs = set([r.blog.id for r in r | inner_r ])
                if len(blogs) < threshold:
                    self.user_rating_matrix[i, j] = 0
                    self.user_coef_matrix[i, j] = 0
                else:
                    vals_outer = r.filter(blog_id__in=blogs).order_by('blog_id').values('general_ratings')
                    vals_inner = inner_r.filter(blog_id__in=blogs).order_by('blog_id').values('general_ratings')
                    self.user_rating_matrix[i, j] = np.corrcoef(vals_inner.T[0], vals_outer.T[0])[0,1]
                    self.user_coef_matrix[i, j] = np.corrcoef(usf.get_fields_arr(), usf.get_fields_arr())[0,1]

        self.user_rating_matrix += self.user_rating_matrix.T
        self.user_coef_matrix += self.user_coef_matrix.T

    def calc_blog_matrix(self):
        for i, bl in enumerate(Blog):
            r = Rating.objects.filter(blog=bl)
            for j, inner_bl in enumerate(self.blogs[i+1:]):
                inner_r = Rating.objects.filter(blog=inner_bl)
                users = ser([r.user.id for r in r | inner_r ])
                if len(users) < threshold:
                    self.blog_matrix[i, j] = 0
                else:
                    vals_outer = r.filter(blog_id__in=users).order_by('user_id').values('general_ratings')
                    vals_inner = inner_r.filter(blog_id__in=users).order_by('user_id').values('general_ratings')
                    self.blog_matrix[i, j] = np.corrcoef(vals_inner.T[0], vals_outer.T[0])[0, 1]

        self.blog_matrix += self.blog_matrix.T

    def most_similar(self):
        pass

    def blog_regression(self, iterations=int(1e3), alpha=1e-3, reg=1e-3):
        for bl in self.blogs:
            if bl.coefficients == '':
                bl.generate_coefficients()
            weights = bl.retrieve_coefficients()
            ratings = bl.rating_set.all()
            if len(ratings) < threshold:
                continue
            X = np.zeros((ratings.shape[0], len(fields)-1))
            for i, r in enumerate(ratings):
                X[i, ] = UserFollowings.objects.get(user=r.user).get_fields_arr()

            X = np.concatenate([np.repeat(1, X.shape[0])[None].T, X], axis=1)
            ratings = np.asarray(ratings.values_list('general_ratings'))
            y = np.zeros((ratings.shape[0], 3))
            for i in range(ratings.shape[0]):
                y[i, ratings[i]] = 1

            while iterations:
                iterations -= 1

                scores = np.dot(X, weights.T)
                exp_scores = np.exp(scores)
                softmax = exp_scores / np.sum(exp_scores, axis=1)[None].T

                derivatives = softmax
                derivatives[:, y] -= 1
                der_weights = np.dot(X.T, derivatives)
                weights -= alpha*der_weights + reg*weights
            bl.set_coeffcients(weights)


    def users_who_liked_also_liked(self):
        users = UserFollowings.objects.all()
        all = users.count()
        for i, bl in enumerate(self.blogs):
            first = Rating.objects.filter(blog=bl)
            if first.count() < threshold:
                self.liking_matrix = np.zeros(self.b)
                continue
            positive_outer = first.filter(general_ratings=2).count()
            for j, inner_bl in enumerate(self.blogs):
                positive_both = 0
                positive_inner_neg_outer = 0
                for us in users:
                    r = us.rating_set.all()
                    if r.filter(general_ratings=2, blog__in=[inner_bl, bl]).count() == 2:
                        positive_both += 1
                    if r.filter(general_ratings__in=[0,1], blog=bl).exists() and r.filter(general_ratings=2, blog=inner_bl).exists():
                        positive_inner_neg_outer += 1

                numerator = positive_both/positive_outer
                denominator = positive_inner_neg_outer/(all-positive_outer)
                self.liking_matrix[i, j] = numerator/denominator


    def predict_rating(self, blog, user):
        user_coef = UserFollowings.objects.get(user=user).get_fields_arr()
        weights = blog.retrieve_coefficients()
        scores = np.dot(user_coef, weights.T)
        #weighted average of user ratings
        loc = dict( [ reversed(i) for i in self.user_dict.items() ] )[user.id]
        where_pos_rat = np.where(self.user_rating_matrix[loc, ] > 0)
        where_pos_coef = np.where(self.user_coef_matrix[loc, ] > 0)
        weights_ratings = np.asarray( [(Rating.objects.get(user_id=self.user_dict[i]).general_ratings, self.user_rating_matrix[loc, i] ) for i in where_pos_rat] )
        score_ratings = np.average(weights_ratings[:, 0], weights=weights_ratings[:, 1])

        weights_ratings = np.asarray( [(Rating.objects.get(user_id=self.user_dict[i]).general_ratings, self.user_coef_matrix[loc, i] ) for i in where_pos_coef] )
        score_coefs = np.average(weights_ratings[:, 0], weights=weights_ratings[:, 1])

        if not PredictRating.object.filter(blog=blog, user=user).exists():
            c = PredictRating(blog=blog, user=user, rating=np.mean(np.argmax(scores), score_ratings, score_coefs))
            c.save()
        else:
            c = PredictRating.object.get(blog=blog, user=user)
            c.rating = np.mean(np.argmax(scores), score_coefs, score_ratings)
            c.save()



class PredictRating(models.Model):
    blog = models.OneToOneField(Blog)
    user = models.OneToOneField(User)
    rating = models.FloatField()

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
            self.last_eval = timezone.now()
            self.save()
            return False
        else:
            return True

    def evaluate(self):
        print('calculations of categories ongoing')
        if self.category == 'general_ratings':
            things = most_popular()
        else:
            things = most_popular_category(category=self.category)
        if self.blogs.all().count():
            self.blogs.remove(*self.blogs.all())
        self.blogs.add(*things)



def followed_users_liked(userfollowings):
    followed_users = userfollowings.following.all()
    blogs_qs = Rating.objects.none()
    for user in followed_users:
        ratings = Rating.objects.filter(user=user, general_ratings=2)
        blogs_qs = blogs_qs | ratings

    blogs_qs = blogs_qs.order_by('-timestamp')[:10]
    bl = list(set([x.blog.id for x in blogs_qs]))
    return Blog.objects.filter(id__in = bl)


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

    rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=10), t))
    ar = calculate_temporal_ratings(rat)
    #print(ar)
    order = np.argsort(ar[:, 1], axis=0)[::-1]

    return Blog.objects.filter(id__in=ar[:, 0][order])

def most_popular_category(category):
    t = timezone.now()

    rat = Rating.objects.filter(timestamp__range=(t-timezone.timedelta(weeks=10), t))

    ar = calculate_temporal_ratings(rat)
    blog_list = Blog.objects.none()
    for bl_id in ar[:, 0]:
        ob = Blog.objects.filter(id=bl_id)
        bl = getattr(ob[0], category)
        if bl > 2:
            blog_list = blog_list | ob

    return blog_list


