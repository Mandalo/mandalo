from django import forms

from .models import Assignment, Language


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))
