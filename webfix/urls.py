from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
]
# The hosting account does not expose a separate media alias, so Django serves
# these low-volume editorial assets while WhiteNoise handles collected static files.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

handler400 = 'website.views.error_400'
handler403 = 'website.views.error_403'
handler404 = 'website.views.error_404'
handler500 = 'website.views.error_500'
