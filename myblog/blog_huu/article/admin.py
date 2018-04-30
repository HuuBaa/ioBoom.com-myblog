from django.contrib import admin
from .models import Tag,Article,Comment,UserProfile,Subcomment

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','post_time','author')

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','article','post_time')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class SubcommentAdmin(admin.ModelAdmin):
    list_display = ('author','reply_to','article','post_time')

admin.site.register(Tag,TagAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Subcomment,SubcommentAdmin)