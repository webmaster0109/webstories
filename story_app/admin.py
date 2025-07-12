from django.contrib import admin
from .models import WebStory, WebStorySlide
# Register your models here.

class WebStorySlideInline(admin.TabularInline):
    model = WebStorySlide
    extra = 1
    ordering = ['order']
    sortable_field_name = 'order'
    readonly_fields = ('created_at', 'updated_at')
  
@admin.register(WebStory)
class WebStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'slug')
    inlines = [WebStorySlideInline]
    readonly_fields = ('created_at', 'updated_at')
