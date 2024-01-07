
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from  Authentication.models import CustomUser

class Post(models.Model):
    creater = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField()
    likers = models.ManyToManyField(CustomUser,blank=True , related_name='likes')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"
   
    def edit_post(self, new_text):
        self.content_text = new_text
        
        self.save()
    def append(self, name, value):
        self.name = value




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "replies": [reply.serialize() for reply in self.replies.all()]
        }
    
    def delete_post(self):
        self.delete()