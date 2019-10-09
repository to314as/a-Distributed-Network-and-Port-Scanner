from django.db import models
from django.utils import timezone


# Create your models here.
class Report(models.Model):

    SCAN_TYPE_CHOICES = (
        ('ALIVE', 'Is-Alive'),
        ('FULLTCP', 'Full TCP connect'),
        ('TCPSYN', 'TCP SYN'),
        ('TCPFIN', 'TCP FIN'),
    )
    SCAN_ORDER_CHOICES = (
        ('SEQ', 'Sequential'),
        ('RAND', 'Random'),
    )
    amount_of_nodes = models.IntegerField()
    start_ip = models.CharField(max_length=39)  # max length of ip6 address stored as string
    end_ip = models.CharField(max_length=39)  # max length of ip6 address stored as string
    start_port = models.IntegerField(null=True)
    end_port = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    scan_type = models.CharField(
        max_length=7,
        choices=SCAN_TYPE_CHOICES,
    )
    scan_order = models.CharField(
        max_length=4,
        choices=SCAN_ORDER_CHOICES,
        default='SEQ'
    )


class Record(models.Model):
    ip_port = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_by = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    report_id = models.ForeignKey(Report, related_name='records', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ip_port} {self.status} {self.created_by}'
