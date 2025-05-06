from django.contrib import admin
from .models import *

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'author', 'created_at', 'updated_at', 'total_likes', 'total_dislikes')

admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile)
