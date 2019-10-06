from django.shortcuts import render
from .models import Report

# Create your views here.
def home(request):
    context = {
        'report': Report.objects.last()
    }
    return render(request, 'starboardscanner_app/starboardscanner_app.html', context)
