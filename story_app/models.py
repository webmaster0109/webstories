from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import string
import random
# Create your models here.

def get_short_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(15))
    

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class WebStory(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=20, default=get_short_id, editable=False, unique=True, help_text="Unique identifier for the story, auto-generated.")
    cover_image = models.ImageField(upload_to='cover_images/', help_text="The main image shown before the story starts. Recommended size: 600x1200px.", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Web Story"
        verbose_name_plural = "Web Stories"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
  

class WebStorySlide(BaseModel):
    order = models.PositiveIntegerField(default=1, help_text="Order of the slide in the story. Lower numbers appear first.")
    story = models.ForeignKey(WebStory, related_name='slides', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='slides/', help_text="Image for the slide. Recommended size: 600x1200px.")
    caption = models.TextField(help_text="Caption text overlay for the slide.", blank=True, null=True)

    class Meta:
        verbose_name = "Web Story Slide"
        verbose_name_plural = "Web Story Slides"
        ordering = ['story', 'order']

    def __str__(self):
        return f"Slide {self.order} of '{self.story.title}'"
    
