from django.contrib import admin
from .models import MostPopularByCat, RecommendationBlog, RecommendationUser

# Register your models here.
class MostPopularByCatModelAdmin(admin.ModelAdmin):
    list_display = ['category']

    class Meta:
        model = MostPopularByCat

class RecommendationBlogModelAdmin(admin.ModelAdmin):
    list_display = ['blog']

    class Meta:
        model = RecommendationBlog

class RecommendationUserModelAdmin(admin.ModelAdmin):
    list_display = ['user']

    class Meta:
        model = RecommendationUser

admin.site.register(MostPopularByCat, MostPopularByCatModelAdmin)
admin.site.register(RecommendationBlog, RecommendationBlogModelAdmin)
admin.site.register(RecommendationUser, RecommendationUserModelAdmin)