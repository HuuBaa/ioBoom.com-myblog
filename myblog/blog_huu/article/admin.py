from django.contrib import admin
from .models import Tag,Article,Comment,UserProfile

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','post_time','author')

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','post_time','author')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Tag,TagAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(UserProfile,UserProfileAdmin)