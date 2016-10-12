from django.db import models
from django.db.models import Count
import math as m
from blogs.models import User, Blog

# Create your models here.
votes = [(-1, "downvote"), (1, "upvote")]

class Comment(models.Model):
    user = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    binom = models.FloatField(default=0.5, null=True, blank=True)
    ups = models.IntegerField(null=True, blank=True)
    downs = models.IntegerField(null=True, blank=True)

    parent = models.ForeignKey('self', related_name="children", blank=True, null=True)

    def set_fks(self, user, blog):
        self.user = user
        self.blog = blog


    def class_str(self):
        return 'comment'

    def __str__(self):
        return self.user.username + " on " + self.blog.name

    def set_parent(self, parent):
        self.parent = parent

    def set_binom(self):
        v_set = self.vote_set.all().values('vote').annotate(countvotes=Count('vote'))
        z = {x['vote']:x['countvotes'] for x in v_set}
        if -1 not in z:
            z[-1] = 0
        if 1 not in z:
            z[1] = 0
        s = z[-1] + z[1]
        if s == 0:
            s = 1
        p = z[1]/float(s)
        self.binom = sorted([0, z[1]/s - m.sqrt( p*(1-p)/s ), 1])[1]
        self.ups = z[1]
        self.downs = z[-1]
        self.save()

    class Meta:
        ordering = ['-binom']


class Vote(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    vote = models.IntegerField(choices=votes)

    def set_fks(self, user, comment):
        self.user = user
        self.comment = comment


