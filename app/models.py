from django.db import models
from django.utils import timezone


class Blocklist(models.Model):
    phone_number = models.CharField(max_length=32, db_index=True)
    date_block = models.DateTimeField(default=timezone.now)
    is_block = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    user = models.ForeignKey('Users', null=True)

    def __str__(self):
        return self.phone_number


class Codes(models.Model):
    sms_id = models.CharField(max_length=64, default=None)
    code = models.CharField(max_length=64, db_index=True)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey('Users', null=True)

    def set_is_used(self):
        self.is_used = True

    def __str__(self):
        return self.code


class Users(models.Model):
    name = models.CharField(max_length=64)
    birth_date = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    code = models.ForeignKey(Codes, null=True)
    date_registration = models.DateTimeField(default=timezone.now)
    status = models.ForeignKey('Messages', null=True)

    def __str__(self):
        return self.name

    def status_code(self):
        return self.status

class Messages(models.Model):
    message = models.CharField(max_length=512)
    status = models.CharField(max_length=32, null=True)