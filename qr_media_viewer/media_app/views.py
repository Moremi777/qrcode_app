from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MediaUpload
from .forms import MediaFileForm

def home(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_instance = form.save()
            return redirect('media_display', media_name=media_instance.file_name)
    else:
        form = MediaFileForm()

    return render(request, 'index.html', {'form': form})

def media_display(request, media_name):
    try:
        media_instance = MediaUpload.objects.get(file_name=media_name)
    except MediaUpload.DoesNotExist:
        return HttpResponse("Media not found.", status=404)

    return render(request, 'media_display.html', {'media_instance': media_instance})
