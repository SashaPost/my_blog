from django.db import models
from django.utils import timezone
# import datetime
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
now = timezone.now



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class BlogAuthor(models.Model):

    first_name = models.CharField("First name", max_length = 50, \
        unique=False, blank=True, null=True, help_text="First name")
    last_name = models.CharField("Last name", max_length = 50, \
        unique=False, blank=True, null=True, help_text="Last name")
    nickname = models.CharField(max_length=100, unique=True)
    acc_created = models.DateTimeField(default=timezone.now) #OR datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=f'cover_images/{user_directory_path}')

    def __str__(self):
        return f'{self.nickname}, created: {self.acc_created}'



class BlogPost(models.Model):
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=False, blank=False)
    post_text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"author: {self.author},\npost_title: {self.title}" 



def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

class PostImages(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image',\
        blank=True, null=True, )



class BlogComment(models.Model):

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=280, )
    comment_added = models.DateTimeField(default=timezone.now)
    
