from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import shared_task
from celery import current_app as app
from celery.schedules import crontab
import base64
import http.client

from matplotlib.dates import seconds


@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        crontab(hour=16, minute=46),
        select_winners.s('380636994338'),
        name = 'select winners'
    )

@app.task
def select_winners(arg):
    return arg

@shared_task
def send_sms(number):
    credential = base64.b64encode(b'Lactonia:UHJmf7648ldYb498V4')
    headers = {"Authorization": "Basic " + str(credential, 'utf-8'), "ContentType": "text/xml"}
    xml = """<message>
    	            <service id='single' source='Lactonia' />
    	            <to>""" + number + """</to>
    	            <body content-type='text/plain'>Vitajemo, Vash kod uspishno zarejestrovano, chekajte na rozigrash. Detali: promo-lactonia.com.ua abo 0800210720</body>
    	        </message>"""
    print(xml)
    conn = http.client.HTTPConnection("bulk.startmobile.ua")
    try:
        conn.request(method="POST", url="/clients.php", body=xml, headers=headers)
    except http.client.HTTPException as err:
        print(err)
    resp = conn.getresponse()
    return resp.read()

