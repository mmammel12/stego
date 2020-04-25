import os

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from textToImage.textIntoImage import (
    decodeText1Bit,
    decodeText2Bit,
    decodeText4Bit,
    decodeText4BitChecksum,
    encodeText1Bit,
    encodeText2Bit,
    encodeText4Bit,
    encodeText4BitChecksum,
)

from stego.forms import TextToImageDecryptForm, TextToImageEncryptForm


def input_encrypt(request):

    # This is where the images are stored when deployed.
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    # create a form instance and populate it with data from the request:
    encryptForm = TextToImageEncryptForm(request.POST, request.FILES)

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        if encryptForm.is_valid():
            textContent = request.FILES["text"].read().decode("utf-8")

            with open(f"{settings.MEDIA_ROOT}/upload.png", "wb+") as destination:
                for chunk in request.FILES["image"].chunks():
                    destination.write(chunk)
            bits = int(encryptForm.cleaned_data["bits"])
            checksum = encryptForm.cleaned_data["checksum"]

            encrypt_map = {1: encodeText1Bit, 2: encodeText2Bit, 4: encodeText4Bit}

            checksum_encrypt_map = {4: encodeText4BitChecksum}

            if checksum:
                checksum_encrypt_map[bits](textContent)
            else:
                encrypt_map[bits](textContent)

            # redirect to a new URL:
            return HttpResponseRedirect("/textToImage/encrypt/")

        else:
            messages.error(
                request,
                "Invalid form entry - Please upload a <strong>.txt</strong> file and set the number of bits.",
            )

    # if a GET (or any other method) we'll create a blank form
    encryptForm = TextToImageEncryptForm()

    return render(
        request,
        "textToImageTemplate/textToImageEncryptInput.html",
        {"encryptForm": encryptForm},
    )


def input_decrypt(request):

    # This is where the images are stored when deployed.
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    decryptForm = TextToImageDecryptForm(request.POST, request.FILES)

    if request.method == "POST":
        if decryptForm.is_valid():
            with open(f"{settings.MEDIA_ROOT}/encoded.png", "wb+") as destination:
                for chunk in request.FILES["image"].chunks():
                    destination.write(chunk)

            bits = int(decryptForm.cleaned_data["bits"])
            checksum = decryptForm.cleaned_data["checksum"]

            decrypt_map = {1: decodeText1Bit, 2: decodeText2Bit, 4: decodeText4Bit}

            checksum_decrypt_map = {4: decodeText4BitChecksum}

            if checksum:
                message = checksum_decrypt_map[bits]()
            else:
                message = decrypt_map[bits]()

            messages.success(request, message)

            return HttpResponseRedirect("/textToImage/decrypt/")

        else:
            messages.error(
                request, "Invalid form entry - Please set the number of bits."
            )

    decryptForm = TextToImageDecryptForm()

    return render(
        request,
        "textToImageTemplate/textToImageDecryptInput.html",
        {"decryptForm": decryptForm},
    )


def encrypt(request):

    context = {"image": f"{settings.MEDIA_URL}/encoded.png"}
    return render(request, "textToImageTemplate/textToImageEncrypted.html", context)


def decrypt(request):

    return render(request, "textToImageTemplate/textToImageDecrypted.html")
