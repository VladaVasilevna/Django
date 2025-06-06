from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from catalog.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("", include("catalog.urls", namespace="catalog")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("users/", include("users.urls", namespace="users")),
    path("mailing/", include("mailing.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
