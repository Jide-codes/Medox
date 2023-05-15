from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media', null=True)
    

    def get_absolute_url(self):
        return reverse("blog:author_profile", kwargs={"pk": self.pk})
    
    @property
    def user_bio(self):
        if self.bio:
            return self.bio
        else:
            return ''
        

    @property
    def avatarUrl(self):
        try:
            url = self.avatar.url
            
        except:
            url =''
        return url
    

class Tag(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft',),
        ('published', 'Published',),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts', null=True)
    body = models.TextField()
    image = models.ImageField(upload_to='media', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default= 'draft')
    tags = models.ManyToManyField(Tag)

    @property
    def image_url(self):
        try: 
            url = self.image.url 
        except:
            url = ''

        return url



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month, 
                                                 self.publish.day, 
                                                 self.slug])
      
        
    @property
    def author_image(self):
        try: 
            url = self.author.avatar.url
            
        except:
            url = ''
        
        return url





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    commenter_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)


    def __str__(self):
        return f'Comment by {self.commenter_name} on {self.post}'
    @property
    def commenter_image(self):
        try:
            url = self.commenter_name.avatar.url
        except:
            url = ''
        return url