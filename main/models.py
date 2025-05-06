from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.timezone import now


class Category(models.Model):
    name=models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name
    
class UserCategory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    class Meta:
        unique_together=('user','category')
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    last_seen=models.DateTimeField(default=now)
    following=models.ManyToManyField('self',related_name='followers',blank=True)
    interests=models.ManyToManyField(Category,related_name='intersted_categories',blank=True)
    
    
    def __str__(self):
        return self.user.username
    

class BlogPost(models.Model):
    blog_title=models.CharField(max_length=255)
    content=CKEditor5Field(config_name='extends')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts_author')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    dislikes=models.ManyToManyField(User,related_name='dislikes',blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='posts_comments')
    content=models.TextField()
    guest_name = models.CharField(max_length=100, blank=True, null=True) 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_likes=models.ManyToManyField(User,related_name='likes_comment',blank=True)
    comment_dislikes=models.ManyToManyField(User,related_name='dislikes_comment',blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f"Commented by {self.user.username} on {self.post.blog_title}"
        else:
            return f"Commented by {self.guest_name} on {self.post.blog_title}"


