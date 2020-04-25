# Create your views here.
import os

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from imageToImage.imageIntoImage import (
    decodeImage1Bit,
    decodeImage2Bit,
    decodeImage4Bit,
    encodeImage1Bit,
    encodeImage2Bit,
    encodeImage4Bit,
)

from stego.forms import ImageToImageDecryptForm, ImageToImageEncryptForm


def input_encrypt(request):

    error = ""
    # This is where the images are stored when deployed.
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    # create a form instance and populate it with data from the request:
    encryptForm = ImageToImageEncryptForm(request.POST, request.FILES)

    # if this is a POST request we need to process the form data
    if request.method == "POST":

        if encryptForm.is_valid():

            with open(f"{settings.MEDIA_ROOT}/upload_inner.png", "wb+") as destination:
                for chunk in request.FILES["inner_image"].chunks():
                    destination.write(chunk)

            with open(f"{settings.MEDIA_ROOT}/upload_outer.png", "wb+") as destination:
                for chunk in request.FILES["outer_image"].chunks():
                    destination.write(chunk)

            bits = int(encryptForm.cleaned_data["bits"])
            encrypt_map = {1: encodeImage1Bit, 2: encodeImage2Bit, 4: encodeImage4Bit}

            try:
                encrypt_map[bits]()
                return HttpResponseRedirect("/imageToImage/encrypt/")
            except ValueError:
                error = "Invalid form entry - Incompatible images."

    if error:
        messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    encryptForm = ImageToImageEncryptForm()

    return render(
        request,
        "imageToImageTemplate/imageToImageEncryptInput.html",
        {"encryptForm": encryptForm},
    )


def input_decrypt(request):

    # This is where the images are stored when deployed.
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    decryptForm = ImageToImageDecryptForm(request.POST, request.FILES)

    if request.method == "POST":
        if decryptForm.is_valid():
            with open(f"{settings.MEDIA_ROOT}/encoded.png", "wb+") as destination:
                for chunk in request.FILES["image"].chunks():
                    destination.write(chunk)

            bits = int(decryptForm.cleaned_data["bits"])
            decrypt_map = {1: decodeImage1Bit, 2: decodeImage2Bit, 4: decodeImage4Bit}
            decrypt_map[bits]()

            return HttpResponseRedirect("/imageToImage/decrypt/")

    decryptForm = ImageToImageDecryptForm()
    return render(
        request,
        "imageToImageTemplate/imageToImageDecryptInput.html",
        {"decryptForm": decryptForm},
    )


def encrypt(request):

    context = {"image": f"{settings.MEDIA_URL}/encoded.png"}
    return render(request, "imageToImageTemplate/imageToImageEncrypted.html", context)


def decrypt(request):
    context = {"image": f"{settings.MEDIA_URL}/decoded.png"}
    return render(request, "imageToImageTemplate/imageToImageDecrypted.html", context)
