from django import forms
from .models import MediaUpload

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['media', 'qr_code']
