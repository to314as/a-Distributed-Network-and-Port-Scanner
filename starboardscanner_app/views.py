from django.shortcuts import render
from .models import Report, Record
from rest_framework import viewsets
from .serializers import ReportSerializer, RecordSerializer


# Create your views here.
def home(request):
    context = {
        'report': Report.objects.last()
    }
    return render(request, 'starboardscanner_app/starboardscanner_app.html', context)


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reports to be viewed or edited.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class RecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows records to be viewed or edited.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
