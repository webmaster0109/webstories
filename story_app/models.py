from django.db import models
from django.urls import reverse
import string
import random

from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os
# Create your models here.

def get_short_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(15))

def optimize_image(image_field, target_kb=100, max_width=1000):
    try:
        img = Image.open(image_field)

        if img.width > max_width:
            new_height = int((max_width / img.width) * img.height)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        if img.mode == 'RGBA':
            img = img.convert('RGB')
        buffer = BytesIO()
        quality = 85
        img.save(buffer, format='WEBP', quality=quality, optimize=True)
        
        while buffer.tell() / 1024 > target_kb and quality > 10:
            buffer = BytesIO()
            quality -= 5
            img.save(buffer, format='WEBP', quality=quality, optimize=True)
        
        original_filename = os.path.splitext(image_field.name)[0]
        new_filename = f"{original_filename}.webp"

        return ContentFile(buffer.getvalue(), name=new_filename)
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return None   

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
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = WebStory.objects.get(pk=self.pk)
                if old_instance.cover_image != self.cover_image:
                    optimized_image = optimize_image(self.cover_image)
                    if optimized_image:
                        self.cover_image = optimized_image
                    else:
                        self.cover_image = old_instance.cover_image
                    super().save(*args, **kwargs)
                    return
            except WebStory.DoesNotExist:
                pass
        if self.cover_image:
            optimized_image = optimize_image(self.cover_image)
            if optimized_image:
                self.cover_image = optimized_image
        super().save(*args, **kwargs)
  

class WebStorySlide(BaseModel):
    order = models.PositiveIntegerField(default=1, help_text="Order of the slide in the story. Lower numbers appear first.")
    story = models.ForeignKey(WebStory, related_name='slides', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='slides/', help_text="Image for the slide. Recommended size: 600x1200px.", null=True, blank=True)
    caption = models.TextField(help_text="Caption text overlay for the slide.", blank=True, null=True)

    class Meta:
        verbose_name = "Web Story Slide"
        verbose_name_plural = "Web Story Slides"
        ordering = ['story', 'order']

    def __str__(self):
        return f"Slide {self.order} of '{self.story.title}'"
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = WebStorySlide.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    optimized_image = optimize_image(self.image)
                    if optimized_image:
                        self.image = optimized_image
                    else:
                        self.image = old_instance.image
                    super().save(*args, **kwargs)
                    return
            except WebStorySlide.DoesNotExist:
                pass
        if self.image:
            optimized_image = optimize_image(self.image)
            if optimized_image:
                self.image = optimized_image
        super().save(*args, **kwargs)
    
