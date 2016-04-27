from django.contrib import admin
from .models import Post
from blog.models import Tag, Category, Comment, Like,UserProfile

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(UserProfile)