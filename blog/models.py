from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)
    
    
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    title = models.CharField(max_length=50)
    body = models.TextField()
    slug = models.SlugField()
    status = models.CharField(max_length=2
                                ,choices=Status.choices,
                                default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[
                        self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug
                        ])

