from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (BlogPostCreateView, BlogPostDeleteView, BlogPostDetailView, BlogPostListView, BlogPostUpdateView,
                    HomePageView)

app_name = "blog"

urlpatterns = [
    path("", HomePageView.as_view(), name="base"),
    path("all_posts/", BlogPostListView.as_view(), name="all_posts"),
    path("post/<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    path("post/new/", BlogPostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", BlogPostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogPostDeleteView.as_view(), name="post_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
