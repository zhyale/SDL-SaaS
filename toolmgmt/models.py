from django.db import models

# Create your models here.
class IpSegment(models.Model):
    ip_start=models.GenericIPAddressField()
    ip_end=models.GenericIPAddressField()
    start_int=models.BigIntegerField(default=0)
    end_int=models.BigIntegerField(default=0)
    address=models.CharField(max_length=256, null=True, blank=True)
