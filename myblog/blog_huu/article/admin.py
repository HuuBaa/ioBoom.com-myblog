from django.contrib import admin
from .models import Tag,Article,Comment,UserProfile

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','post_time','author')

admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(UserProfile)