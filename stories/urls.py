from django.contrib import admin
from django.urls import path
from story_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.story_list, name="story_list"),
    path("visualstories/<str:slug>/", views.story_detail, name="story_detail"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
