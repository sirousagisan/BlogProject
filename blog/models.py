from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
import pytz


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)
    
    
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
    publish = models.DateTimeField(default=timezone.datetime.now(pytz.timezone("Asia/Tokyo")))
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


class Comment(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE,
                            related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"])
        ]
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

class developManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=developed.Status.PUBLISHED)

class developed(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    image = models.ImageField()
    body = models.TextField()
    publish = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.DRAFT)
    Published = developManager()

class FormModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    enquiry = models.TextField()
    def __str__(self) -> str:
        return f"from {self.name}"