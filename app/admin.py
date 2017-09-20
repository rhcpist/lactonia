import csv
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from rangefilter.filter import DateTimeRangeFilter
from .models import Blocklist
from .models import Codes
from .models import Users

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"


def export_users_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistic.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message'])
    users_data = queryset.values_list('id', 'name', 'phone_number', 'birth_date', 'city', 'code_id__code', 'date_registration', 'status_id__message')
    for user_data in users_data:
        writer.writerow(user_data)
    return response
export_users_data.short_description = 'Export to csv'

# Register your models here.
class UsersAdmin(admin.ModelAdmin):

    def status_message(self, instance):
        return instance.status.message


    list_display = (('name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message'))
    # define which columns displayed in changelist))
    readonly_fields = ['name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message']
    # add filtering by date
    list_filter = (
        'status_id__status',
        ('date_registration', DateTimeRangeFilter),
    )
    date_hierarchy = 'date_registration'
    # add searching by fields
    search_fields = ['phone_number', 'code_id__code' ]
    # update actions list - adding export csv data
    actions = [export_users_data,]

admin.site.disable_action('delete_selected')
admin.site.register(Users, UsersAdmin)