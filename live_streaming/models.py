from django.db import models
from django.utils import timezone
# Create your models here.

class LiveStream(models.Model):
  title = models.CharField(max_length=255)
  stream_key = models.CharField(max_length=255, unique=True)
  is_live = models.BooleanField(default=False)
  hls_url = models.URLField(blank=True, null=True)
  thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
  scheduled_start = models.DateTimeField(blank=True, null=True)
  scheduled_end = models.DateTimeField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title
  
  def is_scheduled_to_start(self):
    return self.scheduled_start and self.scheduled_start <= timezone.now()

