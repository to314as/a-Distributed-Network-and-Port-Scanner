from django.forms import ModelForm
from .models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['amount_of_nodes', 'start_ip', 'end_ip', 'start_port', 'end_port', 'scan_type', 'scan_order']
