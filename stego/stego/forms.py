from django import forms
from django.core.validators import FileExtensionValidator

BIT_CHOICES = [(1, "1 bit"), (2, "2 bits"), (4, "4 bits")]


class TextToImageEncryptForm(forms.Form):
    text = forms.FileField(
        label="Text to be Hidden",
        validators=[FileExtensionValidator(allowed_extensions=["txt"])],
    )
    image = forms.ImageField(label="Image to Use")
    bits = forms.ChoiceField(
        choices=BIT_CHOICES, widget=forms.RadioSelect, required=True
    )
    checksum = forms.BooleanField(label="Checksum", required=False)


class TextToImageDecryptForm(forms.Form):
    image = forms.ImageField(label="Image to Decrypt")
    bits = forms.ChoiceField(
        choices=BIT_CHOICES, widget=forms.RadioSelect, required=True
    )
    checksum = forms.BooleanField(label="Checksum", required=False)


class ImageToImageEncryptForm(forms.Form):
    inner_image = forms.ImageField(label="Inner Image")
    outer_image = forms.ImageField(label="Outer Image")
    bits = forms.ChoiceField(
        choices=BIT_CHOICES, widget=forms.RadioSelect, required=True
    )


class ImageToImageDecryptForm(forms.Form):
    image = forms.ImageField(label="Image to Decrypt")
    bits = forms.ChoiceField(
        choices=BIT_CHOICES, widget=forms.RadioSelect, required=True
    )
