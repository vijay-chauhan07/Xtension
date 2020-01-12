
from __future__ import unicode_literals
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager() #default manager
    published = PublishedManager() #custom manager
    STATUS_CHOICES =(
        ('draft', 'Draft'),
        ('published','Published'),
    )

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='blog_posts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = TaggableManager()
    restrict_comment = models.BooleanField(default=False)


    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count() 
        
           
    def get_absolute_url(self):
       return reverse("blog:post_detail", args=[self.id,self.slug])


@receiver(pre_save, sender=Post)       
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug        








class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    dob = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    mobile = models.CharField(default=0, max_length=10)
    photo = models.ImageField(upload_to='profile_image', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)


    def __str__(self):
        return "Profile of user {}".format(self.user.username)
    
    def total_followers(self):
         return self.followers.count() 
    
     

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return "{}-{}".format(self.post.title, str(self.user.username))      




   

    


    


        
class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    def __unicode__(self):
        return self.post.title + "image"

    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)    

        if self.image:
            try:
                image = Image.open(self.image.path)
                if image.height > 300 or image.width > 300:
                    new_img =(300, 300)
                    image.thumbnail(new_img)
                    image.save(self.image.path)

                
            except Images.DoesNotExist:
                pass
            
                   
        

 
        
        
class TotalViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='totalviews')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return "{}".format(self.post.title)



