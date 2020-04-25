from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path

from . import settings, views

urlpatterns = [
    path("", views.index, name="index"),
    path("imageToImage/", include("imageToImage.urls")),
    path("textToImage/", include("textToImage.urls")),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
