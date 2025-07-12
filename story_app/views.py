from django.shortcuts import render, get_object_or_404
from .models import WebStory
# Create your views here.


def story_list(request):
  stories = WebStory.objects.filter(is_active=True).order_by('-created_at')

  return render(request, 'index.html', {'stories': stories})

def story_detail(request, slug):

  story = get_object_or_404(
    WebStory.objects.prefetch_related('slides'),
    slug=slug,
    is_active=True
  )

  return render(request, 'story_detail.html', {'story': story})