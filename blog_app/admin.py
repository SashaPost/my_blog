from django.contrib import admin
from .models import (
    BlogAuthor, 
    BlogPost, 
    PostImages, 
    BlogComment,
    )

# Register your models here.
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nickname', 'acc_created',\
        'bio', 'avatar']
    prepopulated_fields = {'slug': ('nickname', )}

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'post_text', 'date_posted']
    prepopulated_fields = {'slug': ('title', )}
    pass



# admin.site.register(BlogAuthor)
admin.site.register(BlogAuthor, BlogAuthorAdmin)
# admin.site.register(BlogPost)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(PostImages)
admin.site.register(BlogComment)
