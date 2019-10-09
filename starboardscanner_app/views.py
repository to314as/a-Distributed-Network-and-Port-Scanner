import random
import requests
import time

from django.shortcuts import render
from rest_framework import viewsets

from .models import Report, Record
from .serializers import ReportSerializer, RecordSerializer


# Create your views here.
def home(request):
    context = {
        'report': Report.objects.last()
    }
    return render(request, 'starboardscanner_app/starboardscanner_app.html', context)


def request_page(request):
    if request.GET.get('submit_job_btn'):
        amount_of_nodes = request.GET.get('amountOfNodes')
        start_ip = request.GET.get('startIP')
        end_ip = request.GET.get('endIP')
        start_port = request.GET.get('startPort')
        end_port = request.GET.get('endPort')
        scan_type = request.GET.get('scanType')
        scan_order = request.GET.get('scanOrder')

        current_report = Report(amount_of_nodes=amount_of_nodes, start_ip=start_ip, end_ip=end_ip,
                                start_port=start_port,
                                scan_type=scan_type, scan_order=scan_order)
        current_report.save()

        containers_dict_send = {}
        containers_dict_diff = {}
        for i in range(amount_of_nodes):
            containers_dict_send[f'container_{i}'] = 0
            containers_dict_diff[f'container_{i}'] = 0
            # create containers

        job_list = []
        start_ip_end = [int(x) for x in map(str.strip, start_ip.split('.')) if x][-1]
        end_ip_end = [int(x) for x in map(str.strip, end_ip.split('.')) if x][-1]
        for ip in range(start_ip_end, end_ip_end + 1):
            for port in range(start_port, end_port + 1):
                curr_ip_port = start_ip[:-len(str(start_ip_end))] + str(ip) + ":" + str(port)
                job_list.append(curr_ip_port)

        if scan_order is 'Random' or 'RAND':
            print(scan_order)
            random.shuffle(job_list)

        start_time_job = time.process_time()
        for job in job_list:
            for key, value in containers_dict_send.items():
                received_cnt = Record.objects.filter(created_by=key).count()
                containers_dict_diff[key] = containers_dict_send[key] - received_cnt
            container = min(containers_dict_diff, key=containers_dict_diff.get)
            containers_dict_send[container] += 1
            job = {
                'ip_port': job,
                'scan_type': scan_type,
                'report_id': Report.ojects.latest('pk').pk,
            }

            job_endpoint_of_flask_scanningnode = f'127.0.0.1:{5000 + int(container[-1])}'  # depends on container
            res = requests.post(job_endpoint_of_flask_scanningnode, json=job)
        end_time_job = time.process_time()
        Report.objects.filter(pk=Report.ojects.latest('pk')).update(execution_time=(end_time_job - start_time_job))

    context = {'report': Report.objects.latest()}

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
