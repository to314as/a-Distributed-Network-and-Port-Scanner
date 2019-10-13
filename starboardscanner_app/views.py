import random
import signal
import requests
import time
import os
import logging
import sys
import subprocess
import time

from django.shortcuts import render
from rest_framework import viewsets
from django.template import RequestContext
from .models import Report, Record
from .serializers import ReportSerializer, RecordSerializer
from .forms import ReportForm, LogForm
from django.views.decorators.csrf import ensure_csrf_cookie

logging.basicConfig(level=logging.DEBUG)


#
# #Af Create your views here.
# def home(request):
#     print("home")
#     print(request.GET.get('submit_job_btn'))
#     if request.GET.get('request_log_btn') == 'Clicked':
#         print("Request log button clicked")
#         context = Report.objects.get(pk=request.GET.get('logID')),
#         return render(request, 'starboardscanner_app/starboardscanner_app.html', context)
#     return render(request, 'starboardscanner_app/starboardscanner_app.html', context)

@ensure_csrf_cookie
def home(request):
    if request.method == 'POST':
        if request.POST.get("request_log_btn"):
            form = LogForm(request.POST)
            if form.is_valid():
                print('requesting log')
                print(form.cleaned_data['logID'])
                if form.cleaned_data['logID'] > Report.objects.last().pk:
                    report_id = Report.objects.last().pk
                else:
                    report_id = form.cleaned_data['logID']
                context = {'report': Report.objects.get(pk=report_id), 'form_logID': LogForm(), 'form_input':ReportForm()}
                return render(request, 'starboardscanner_app/starboardscanner_app.html', context)
        elif request.POST.get("execute_job_btn"):
            form = ReportForm(request.POST)
            if form.is_valid():
                print("Submit button clicked")
                amount_of_nodes = form.cleaned_data['amount_of_nodes']
                start_ip = form.cleaned_data['start_ip']
                end_ip = form.cleaned_data['end_ip']
                start_port = form.cleaned_data['start_port']
                end_port = form.cleaned_data['end_port']
                scan_type = form.cleaned_data['scan_type']
                scan_order = form.cleaned_data['scan_order']

                current_report = Report(amount_of_nodes=amount_of_nodes, start_ip=start_ip, end_ip=end_ip,
                                        start_port=start_port, end_port=end_port,
                                        scan_type=scan_type, scan_order=scan_order)
                current_report.save()
                print("report template saved")
                containers_dict_send = {}
                containers_dict_diff = {}
                # os.chdir(os.path.abspath(os.path.dirname(__file__)))
                # os.chdir('..')
                # os.chdir('network')
                # os.chdir('/home/tobias/networkscanner/network')  # adjust to your path
                # os.system('docker build -t n .')
                # os.chdir(os.path.abspath(os.path.dirname(__file__)))
                # os.chdir('..')
                # os.chdir('victim')
                # os.system(f'python create_victim.py {start_ip}')
                # print('creating nodes')
                processes = []
                for i in range(amount_of_nodes):
                    containers_dict_send[f'container_{5000 + i}'] = 0
                    containers_dict_diff[f'container_{5000 + i}'] = 0
                    # os.system(f'docker run -p {50000+i}:{50000+i} --name container_{i} n python job_processor.py container_{i} &')
                    print(f'{sys.executable} {os.path.abspath(os.path.dirname(__file__))}\\job_processor.py')
                    a_subprocess = subprocess.Popen([f'{sys.executable}', f'{os.path.abspath(os.path.dirname(__file__))}\\job_processor.py', f'-p {5000 + i}', f'-i {Report.objects.last().pk}'])
                    processes.append(a_subprocess)
                print('nodes created')
                job_list = []
                start_ip_end = [int(x) for x in map(str.strip, start_ip.split('.')) if x][-1]
                end_ip_end = [int(x) for x in map(str.strip, end_ip.split('.')) if x][-1]
                for ip in range(start_ip_end, end_ip_end + 1):
                    for port in range(start_port, end_port + 1):
                        curr_ip_port = start_ip[:-len(str(start_ip_end))] + str(ip) + ":" + str(port)
                        job_list.append(curr_ip_port)
                print('job list created')
                if scan_order == 'RAND':
                    print(scan_order)
                    random.shuffle(job_list)
                current_time_wait = time.time()
                while time.time() - current_time_wait < amount_of_nodes:
                    continue
                start_time_job = time.process_time()


                for job in job_list:
                    for key, value in containers_dict_send.items():
                        received_cnt = Record.objects.filter(created_by=key).count()
                        containers_dict_diff[key] = containers_dict_send[key] - received_cnt
                    # container = max(containers_dict_diff, key=containers_dict_diff.get)
                    container = min(containers_dict_send, key=containers_dict_send.get)
                    print(container)
                    containers_dict_send[container] += 1

                    job = {
                        'ip_port': job,
                        'scan_type': scan_type,
                        'report_id': Report.objects.last().pk,
                    }

                    job_endpoint_of_flask_scanningnode = f'http://127.0.0.1:{container.split("_")[-1]}'  # depends on container
                    res = requests.post(job_endpoint_of_flask_scanningnode, json=job)
                end_time_job = time.process_time()
                print('jobs send')
                Report.objects.filter(pk=Report.objects.last().pk).update(execution_time=(end_time_job - start_time_job))
                context = {'report': Report.objects.last(), 'form_logID': LogForm(), 'form_input': ReportForm()}
                print('rendering new context')
                for flask_process in processes:
                    flask_process.kill()
                return render(request, 'starboardscanner_app/starboardscanner_app.html', context)
    # # process the data in form.cleaned_data
    else:
        print("rendering latest report")
        context = {'report': Report.objects.last(), 'form_logID': LogForm(),
                   'form_input': ReportForm()}
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
