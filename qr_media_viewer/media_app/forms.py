from django import forms
from .models import MediaUpload

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaUpload
        fields = ['media', 'qr_code']
