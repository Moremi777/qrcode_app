from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import MediaFileForm
from .utils import generate_qr_code
from .models import MediaUpload

def home(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_instance = form.save()
            return render(request, 'index.html', {
                'form': form,
                'qr_code_url': media_instance.qr_code.url,
                'media_name': media_instance.media.name,
            })
    else:
        form = MediaFileForm()

    return render(request, 'index.html', {'form': form})


from django.shortcuts import render
from .models import MediaUpload


def media_display(request, media_name):
    # Retrieve media object based on media_name
    media = MediaUpload.objects.get(file_name=media_name)
    return render(request, 'media_display.html', {'media': media})
