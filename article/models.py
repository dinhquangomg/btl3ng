from django.db import models
from ckeditor.fields import RichTextField 
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, default=None)
    thumbnail = models.ImageField(blank=True, null=True, default=None, upload_to='images/%Y/%m/%d/')
    content = RichTextField(default=None, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag, default=None, null=True, on_delete=models.CASCADE, blank=True)
    likes = models.ManyToManyField(User)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title