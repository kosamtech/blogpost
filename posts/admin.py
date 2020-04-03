from django.contrib import admin
from .models import Post, Author, Category, Comment, AnonymousView, PostView, Contact

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(AnonymousView)
admin.site.register(Contact)

admin.site.index_title = "Sam's Tech Blog"
admin.site.site_header = "Sam's Tech Blog System"
admin.site.site_title = "Welcome to my blog"