from django.contrib import admin
from posts.models import Post, Category, SearchWord, Comment


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(SearchWord)
