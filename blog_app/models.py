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
    avatar = models.ImageField(upload_to=f'cover_images/{user_directory_path}',\
        blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True,\
        unique=True, verbose_name='slug')

    def __str__(self):
        return f'{self.nickname},\ncreated: {self.acc_created}'

    def get_absolute_url(self):
        return reverse("author", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nickname)
        return super().save(*args, **kwargs)
    



def create_post_slug(title):
    slug = slugify(title)
    qs = BlogPost.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" % (slug, qs.first().id)
    return slug

class BlogPost(models.Model):
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=False, blank=False)
    post_text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, null=True, blank=True,\
        unique=True, verbose_name='slug')

    def __str__(self):
        return f"author: {self.author},\npost_title: {self.title}" 

    def get_absolute_url(self):
        return reverse("blog", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_post_slug(self.title)
        return super().save(*args, **kwargs)
    



def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

class PostImages(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image',\
        blank=True, null=True, )
    
    def get_absolute_url(self):
        return reverse("post_image", kwargs={"pk": self.pk})
    



class BlogComment(models.Model):

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=280, )
    comment_added = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("comment", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Comment ID: {self.id},\nWas added: {self.comment_added}"

    
    
    
