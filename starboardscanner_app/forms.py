from django.forms import ModelForm, TextInput
from .models import Report
from django import forms
from crispy_forms.helper import FormHelper

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['amount_of_nodes', 'start_ip', 'end_ip', 'start_port', 'end_port', 'scan_type', 'scan_order']
        widgets = {
            'amount_of_nodes': TextInput(attrs={'placeholder': '10'}),
            'start_ip': TextInput(attrs={'placeholder': '127.1.1.1'}),
            'end_ip': TextInput(attrs={'placeholder': '127.1.1.1'}),
            'start_port': TextInput(attrs={'placeholder': '1'}),
            'end_port': TextInput(attrs={'placeholder': '1023'}),
            # 'scan_type': ,
            # 'scan_order':,
        }


class LogForm(forms.Form):
    logID = forms.IntegerField(label='Log ID')