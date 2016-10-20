from django.shortcuts import get_object_or_404
from blogs.models import Blog
from django.db.models import Q

threshold = 15

def blog_and_user(request, pk=None):
    return request.user, get_object_or_404(Blog, id=pk)

def ugly_filtering(and_or, things):

    if and_or:
        return Blog.objects.filter( Q(general_ratings__gte=things["general_ratings"][0]) &
                             Q(general_ratings__lte=things["general_ratings"][1])&
                             Q(politics__gte=things["politics"][0]) &
                             Q(politics__lte=things["politics"][1])&
                             Q(sports__gte=things["sports"][0]) &
                             Q(sports__lte=things["sports"][1])&
                             Q(culture__gte=things["culture"][0]) &
                             Q(culture__lte=things["culture"][1])&
                             Q(tech__gte=things["tech"][0]) &
                             Q(tech__lte=things["tech"][1])&
                             Q(travel__gte=things["travel"][0]) &
                             Q(travel__lte=things["travel"][1])&
                             Q(fashion__gte=things["fashion"][0]) &
                             Q(fashion__lte=things["fashion"][1])&
                             Q(hard_science__gte=things["hard_science"][0]) &
                             Q(hard_science__lte=things["hard_science"][1])&
                             Q(soft_science__gte=things["soft_science"][0]) &
                             Q(soft_science__lte=things["soft_science"][1]))

    else:
        return Blog.objects.filter(   (Q(general_ratings__gte=things["general_ratings"][0]) &
                                       Q(general_ratings__lte=things["general_ratings"][1]))|
                                      (Q(politics__gte=things["politics"][0]) & Q(politics__lte=things["politics"][1]))|
                                      (Q(sports__gte=things["sports"][0]) & Q(sports__lte=things["sports"][1]))|
                                      (Q(culture__gte=things["culture"][0]) & Q(culture__lte=things["culture"][1]))|
                                      (Q(tech__gte=things["tech"][0]) & Q(tech__lte=things["tech"][1]))|
                                      (Q(travel__gte=things["travel"][0]) & Q(travel__lte=things["travel"][1]))|
                                      (Q(fashion__gte=things["fashion"][0]) & Q(fashion__lte=things["fashion"][1]))|
                                      (Q(hard_science__gte=things["hard_science"][0]) &
                                       Q(hard_science__lte=things["hard_science"][1]))|
                                      (Q(soft_science__gte=things["soft_science"][0]) &
                                       Q(soft_science__lte=things["soft_science"][1])) )


class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2