from __future__ import absolute_import, unicode_literals
from datetime import timedelta, datetime
from celery import shared_task
from celery import current_app as app
from .models import Users, Winners
from django.core import serializers
from django.db.models import Count
import base64
import http.client

from matplotlib.dates import seconds


@app.task
def add(x, y):
    return str(x + y)

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@app.on_after_finalize.connect
def setup_periodic_tasks( sender, **kwargs ):
    sender.add_periodic_task(
        60,
        cron_winners.s('test'),
        name="test"
    )

# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(
#         crontab(hour=15, minute=38),
#         select_winners.s('380636994338'),
#         name = 'select winners',
#     )

@app.task
def cron_winners(arg):
    if datetime.now().hour == 14 and datetime.now().minute == 33 :
        winners = select_winners()
        return winners
    else:
        pass

@shared_task
def select_winners():
    yesterday = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) - timedelta(days=1)
    today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    users_all = Users.objects.filter(date_registration__range=(yesterday, today), status=2).exclude(phone_number='False')
    users_ids_repeated = users_all.values_list('id', flat=True).distinct('phone_number')
    users_ids = Users.objects.filter(id__in=users_ids_repeated).order_by('?')
    count = 0
    for user in users_ids:
        if count < 130:
            winnersModel = Winners(user=user, gift=1)
            text_sms = 'Vitajemo, Vi staly peremozhcem v shhodennomu rozigrashi akcii\' \"Laktonija. Napovny zhyttja zdorov\'jam\". Vash rahunok bude popovneno protjagom 5 dniv.'
            send_sms(user.phone_number, text_sms)
        else:
            winnersModel = Winners(user=user, gift=0)
            text_sms = 'Vybachte, ale Vy ne staly peremozhcem v shhodennomu rozigrashi akcii\' \"Laktonija. Napovny zhyttja zdorov\'jam\". Prodovzhujte pryjmaty uchast\' i nehaj shhastyt\'.'
            send_sms(user.phone_number, text_sms)
        winnersModel.save()
        count += 1
    #data = serializers.serialize('json', users, fields=('id', 'phone_number', 'name', 'date_registration'))
    return users_ids

@shared_task
def send_sms(number, text_sms):
    credential = base64.b64encode(b'Lactonia:UHJmf7648ldYb498V4')
    headers = {"Authorization": "Basic " + str(credential, 'utf-8'), "ContentType": "text/xml"}
    xml = """<message>
    	            <service id='single' source='TECT' />
    	            <to>""" + number + """</to>
    	            <body content-type='text/plain'>""" + text_sms + """</body>
    	        </message>"""
    print(xml)
    conn = http.client.HTTPConnection("bulk.startmobile.ua")
    try:
        conn.request(method="POST", url="/clients.php", body=xml, headers=headers)
    except http.client.HTTPException as err:
        print(err)
    resp = conn.getresponse()
    return resp.read()

