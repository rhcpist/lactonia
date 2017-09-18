from django.contrib import admin
from django.contrib.auth.models import User
from .models import Blocklist
from .models import Codes
from .models import Users

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"

# Register your models here.
class UsersAdmin(admin.ModelAdmin):

    def status_message(self, instance):
        return instance.status.message

    list_display = (('name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message'))
    # define which columns displayed in changelist))
    readonly_fields = ['name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message']
    # add filtering by date
    list_filter = ('status', 'date_registration')

admin.site.register(Users, UsersAdmin)