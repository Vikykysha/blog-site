from django.db import models
from django.utils import timezone
from django.conf import settings 
from django.contrib.auth.models import User


class UserProfile(models.Model):
   
    user = models.OneToOneField(User,null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    
    hobby = models.CharField(blank=True, null=True, max_length=200)
    had_like = models.BooleanField(default=False) 
    had_dislike = models.BooleanField(default=False) 
    
    def __unicode__(self):
        return self.user.username

class Tag(models.Model):
    
    name = models.CharField(max_length=50)
    important = models.BooleanField(default=False) 
         
    
    def __unicode__(self):
        return self.name


class Post(models.Model):
    
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey ('Category',blank=True, null=True)
    tags = models.ManyToManyField(Tag,related_name="tags",blank=True)
    likes  = models.BigIntegerField(blank = True, default = 0)
    dislikes  = models.BigIntegerField(blank = True, default = 0)  
    addLike = models.IntegerField(default = 0)
    glance = models.BigIntegerField(blank = True, default = 0)

    def approved_comment (self):
        return self.comments.filter(approved_comment = True)
 
    def publish(self):
        self.published_date = timezone.now()
        self.save()
      
    def __str__(self):
        return self.title
    
class Category (models.Model):
    
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    

   
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    created_date_on = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
      
class Like(models.Model):       
    like_data = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('auth.User', blank=True, null=True)
    post = models.ForeignKey('Post', blank=True, null=True)                                     
                                     
    

    

       
    
