from django.shortcuts import render

def home(request):
    return render(request, 'vid_stream.html')