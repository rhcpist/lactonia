import csv
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from rangefilter.filter import DateTimeRangeFilter
from .models import Blocklist
from .models import Codes
from .models import Users
from .models import Winners

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"


def export_users_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistic_users.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message'])
    users_data = queryset.values_list('id', 'name', 'phone_number', 'birth_date', 'city', 'code_id__code', 'date_registration', 'status_id__message')
    for user_data in users_data:
        writer.writerow(user_data)
    return response
export_users_data.short_description = 'Export to csv users'

def export_winners_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistic_winners.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'user_name', 'user_phone', 'birth_date', 'city', 'code', 'date_registration'])
    users_data = queryset.values_list('user_id__id', 'user_id__name', 'user_id__phone_number', 'user_id__birth_date', 'user_id__city', 'user_id__code', 'user_id__date_registration')
    for user_data in users_data:
        writer.writerow(user_data)
    return response
export_users_data.short_description = 'Export to csv winners'

# Register your models here.
class UsersAdmin(admin.ModelAdmin):

    def status_message(self, instance):
        return instance.status.message


    list_display = (('name', 'phone_number', 'birth_date', 'city', 'code', 'date_registration', 'status_message'))
    # define which columns displayed in changelist))
    readonly_fields = ['name', 'birth_date', 'city', 'code', 'date_registration', 'status_message']
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

class WinnersAdmin(admin.ModelAdmin):

    def user_phone(self, instance):
        return instance.user.phone_number

    def user_name(self, instance):
        return instance.user.name

    def birth_date(self, instance):
        return instance.user.birth_date

    def city(self, instance):
        return instance.user.city

    def code(self, instance):
        return instance.user.code

    def date_registration(self, instance):
        return instance.user.date_registration

    list_display = (('user_name', 'user_phone', 'birth_date', 'city', 'code' , 'date_registration'))
    readonly_fields = ['user_name', 'user_phone', 'birth_date', 'city', 'code', 'date_registration']
    list_filter = (
        ('user_id__date_registration', DateTimeRangeFilter),
    )
    search_fields = ['user_id__phone_number', 'user_id__code_id__code', 'user_id__date_registration']
    actions = [export_winners_data,]

admin.site.disable_action('delete_selected')
admin.site.register(Users, UsersAdmin)
admin.site.register(Winners, WinnersAdmin)