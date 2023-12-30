from django.contrib import admin
from . models import *


# admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_pic', 'mobile_number')

admin.site.register( CustomUser)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('creater', 'date_created', 'content_text', 'comment_count')
    list_filter = ('date_created', 'comment_count')
    search_fields = ('creater', 'content_text')
    readonly_fields = ('date_created', 'comment_count')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'commenter', 'comment_content', 'comment_time')
    list_filter = ('post', 'commenter', 'comment_time')
    search_fields = ('post__title', 'commenter__username', 'comment_content')
    readonly_fields = ('comment_time',)

    # Optionally, if you want to customize how the model is displayed in the admin panel.
    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

admin.site.register(Comment, CommentAdmin)


""" Username: nzmdn
Email address: nzmdn@gmail.com
Password: nzmdn """