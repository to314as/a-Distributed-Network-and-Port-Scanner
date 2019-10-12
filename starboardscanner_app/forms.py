from django.forms import ModelForm, TextInput
from .models import Report
from django import forms

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['amount_of_nodes', 'start_ip', 'end_ip', 'start_port', 'end_port', 'scan_type', 'scan_order']
        widgets = {
            'amount_of_nodes': TextInput(attrs={'placeholder': 'Amount of Scanning Nodes'}),
            # 'start_ip':,
            # 'end_ip':,
            # 'start_port':,
            # 'end_port':,
            # 'scan_type':,
            # 'scan_order':,
        }


class LogForm(forms.Form):
    logID = forms.IntegerField(label='LogID')