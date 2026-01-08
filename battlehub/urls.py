from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="tournaments:tournament_list", permanent=False)),
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("tournaments/", include(("tournaments.urls", "tournaments"), namespace="tournaments")),
    path("admin-panel/", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),
    # Convenience redirect for a common misspelling
    path("tourments/", RedirectView.as_view(pattern_name="tournaments:tournament_list", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
