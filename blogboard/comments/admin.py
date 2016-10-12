from django.contrib import admin

# Register your models here.
from .models import Comment, Vote

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'blog']
    list_display_links = ['user']

    class Meta:
        model = Comment

class VoteModelAdmin(admin.ModelAdmin):
    list_display = ['comment']
    list_display_links = ['comment']

    class Meta:
        model = Vote


admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Vote, VoteModelAdmin)