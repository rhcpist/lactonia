from __future__ import absolute_import, unicode_literals
from celery import shared_task
import base64
import http.client


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def send_sms(number):
    credential = base64.b64encode(b'senderalert:7Y8Zwj5tvBQPHERw')
    headers = {"Authorization": "Basic " + str(credential, 'utf-8'), "ContentType": "text/xml"}
    xml = """<message>
    	            <service id='single' source='StartMobile' />
    	            <to>""" + number + """</to>
    	            <body content-type='text/plain'>Vitajemo, Vash kod uspishno zarejestrovano, chekajte na rozigrash. Detali: promo-lactonia.com.ua abo 0800210720</body>
    	        </message>"""
    print(xml)
    conn = http.client.HTTPConnection("bulk.startmobile.ua")
    try:
        conn.request(method="POST", url="/client.php", body=xml, headers=headers)
    except http.client.HTTPException as err:
        print(err)
    resp = conn.getresponse()
    return resp