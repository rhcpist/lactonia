from django.db import models
from django.utils import timezone

class Blocklist(models.Model):
    phone_number = models.CharField(max_length=32)
    date_block = models.DateTimeField(default=timezone.now)
    is_block = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.phone_number

class Codes(models.Model):
    sms_id = models.CharField(max_length=64, default=None)
    code = models.CharField(max_length=64)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class Users(models.Model):
    name = models.CharField(max_length=64)
    birth_date = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    code = models.ForeignKey(Codes)
    date_registration = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name