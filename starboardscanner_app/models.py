from django.db import models
from django.utils import timezone


# Create your models here.
class Report(models.Model):
    title = models.TextField()  # type of scan ran
    date_created = models.DateTimeField(default=timezone.now)
    location_status = models.TextField()  # would contain list of tuples with status like (ip:port, status)

    def __str__(self):
        return self.title
