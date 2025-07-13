from django.contrib import admin
from .models import LiveStream

@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'stream_key', 'is_live', 'scheduled_start', 'scheduled_end', 'created_at', 'updated_at')
    search_fields = ('title', 'stream_key')
    list_filter = ('is_live', 'scheduled_start', 'scheduled_end')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True