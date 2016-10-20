from django.contrib import admin
from .models import MostPopularByCat, RecommendationBlog, RecommendationUser, Calculations

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

class CalculationsModelAdmin(admin.ModelAdmin):
    list_display = ['last_calculated']

    class Meta:
        model = Calculations
#
# class ManageCalculationsModelAdmin(admin.ModelAdmin):
#     list_display = ['last_eval', 'last_regression']
#
#     class Meta:
#         model = ManageCalculations

admin.site.register(MostPopularByCat, MostPopularByCatModelAdmin)
admin.site.register(RecommendationBlog, RecommendationBlogModelAdmin)
admin.site.register(RecommendationUser, RecommendationUserModelAdmin)
admin.site.register(Calculations, CalculationsModelAdmin)