from django.urls import path

from . import views

urlpatterns = [
    path("input/encrypt/", views.input_encrypt, name="imageToImageInputEncrypt"),
    path("input/decrypt/", views.input_decrypt, name="imageToImageInputDecypt"),
    path("encrypt/", views.encrypt, name="imageToImageEncrypt"),
    path("decrypt/", views.decrypt, name="imageToImageDecrypt"),
]
