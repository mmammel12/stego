from django.urls import path

from . import views

urlpatterns = [
    path("input/encrypt/", views.input_encrypt, name="textToImageInputEncrypt"),
    path("input/decrypt/", views.input_decrypt, name="textToImageInputDecypt"),
    path("encrypt/", views.encrypt, name="textToImageEncrypt"),
    path("decrypt/", views.decrypt, name="textToImageDecrypt"),
]
