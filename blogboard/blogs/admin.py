from django.contrib import admin
from .models import Blog, Rating, UserFollowings
# Register your models here.
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'language']
    list_display_links = ['name']
    list_filter = ['name', 'language']
    search_fields = ['name', 'language']
    class Meta:
        model = Blog

class RatingModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'general_ratings', 'hard_science', 'soft_science']
    list_filter = ['user', 'blog']
    search_fields = ['user__username', 'blog__name']

    class Meta:
        model = Rating


class UserFollowingsModelAdmin(admin.ModelAdmin):
    list_display = ['user']

    class Meta:
        model = UserFollowings

admin.site.register(Blog, BlogModelAdmin)
admin.site.register(Rating, RatingModelAdmin)
admin.site.register(UserFollowings, UserFollowingsModelAdmin)