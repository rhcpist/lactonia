import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from celery import shared_task
from django.shortcuts import redirect
import re
from .tasks import send_sms

from .models import Blocklist
from .models import Codes
from .models import Users
from .models import Messages


def format_phone(phone):
    phone = re.sub(r'\D', '', phone)
    if phone[0:3] == '380' and len(phone)==12:
        return phone
    elif phone[0:2] == '80' and len(phone)==11:
        return '3'+phone
    elif phone[0] == '0' and len(phone)==10:
        return '38'+phone
    else:
        return False


def index(request):
    return render(request, 'index.html', {'question': 'Hello'})


def win(request):
    template = loader.get_template('win.html')

    context = {
        'winners': 'Hello',
    }
    return HttpResponse(template.render(context, request))


def rules(request):
    template = loader.get_template('rules.html')
    context = {
        'param': 'Hello',
    }
    return HttpResponse(template.render(context, request))


def registration(request):
    if request.method == "POST":

        inputName = str(request.POST.get('inputname'))
        birthDate = str(request.POST.get('birthdate'))
        phoneNumber = format_phone(
            str(request.POST.get('phone'))
        )
        city = str(request.POST.get('city'))
        inputCode = str(request.POST.get('code'))

        userModel = Users(
            name=inputName,
            birth_date=birthDate,
            phone_number=phoneNumber,
            city=city,
            code=None,
            status=None
        )
        #userModel.status = Messages.objects.get(id__exact=1)
        userModel.save()

        blockList = Blocklist(phone_number=phoneNumber, count=0)
        blockList.user = userModel
        try:
            blockList = Blocklist.objects.get(phone_number__exact=phoneNumber)
        except ObjectDoesNotExist:
            pass

        try:
            if blockList.is_block == True and blockList.date_block <= datetime.now() - timedelta(days=1):
                blockList.is_block = False
                blockList.count = 0
                blockList.save()

            if blockList.is_block == True:

                userModel.status = Messages.objects.get(id__exact=4)

                userModel.save()
                blockList.save()

                return render(request, 'registration.html', {'question': 'Заблокованый'})

        except ObjectDoesNotExist:
            pass

        try:
            codeObj = Codes.objects.get(code__exact=inputCode, is_used__exact=False)

            codeObj.is_used = True
            codeObj.user = userModel
            codeObj.save()

            userModel.code = codeObj
            userModel.status = Messages.objects.get(id__exact=2)
            #send sms
            text_sms = 'Vitajemo, Vash kod uspishno zarejestrovano, chekajte na rozigrash. Detali: promo-lactonia.com.ua abo 0800210720'
            print(send_sms(str(userModel.phone_number), text_sms))

            userModel.save()

        except ObjectDoesNotExist:
            userModel.status = Messages.objects.get(id__exact=1)
            userModel.save()
            blockList.count = blockList.count + 1
            if blockList.count > 4 : blockList.is_block = True
            blockList.save()
            return render(request, 'registration.html', {'question': 'Невирный код support@lactoria.ua'})


    return render(request, 'registration.html', {'question': 'Hello'})


@csrf_exempt
def send_code(request):
    if request.method == "POST":
        inputCode = str(request.POST.get('code'))
        inputNumber = str(request.POST.get('number'))
        formatedNum = re.findall('\d+', inputNumber)
        formatedNum = ''.join(formatedNum)

        blockObj = Blocklist(phone_number=formatedNum,count=0)
        try:
            blockObj = Blocklist.objects.get(phone_number__exact=formatedNum)
        except ObjectDoesNotExist:
            pass

        if blockObj.is_block == True:
            print('Blocked')
            return HttpResponse(
                json.dumps(
                    {
                        "is_valid": False,
                        "message": Messages.objects.values_list('message', flat=True).filter(pk=4)[0]
                    }
                ),
                content_type='application/json'
            )
        if len(inputCode) != 9 :
            return HttpResponse(
                json.dumps(
                    {
                        "is_valid": False,
                        "message": Messages.objects.values_list('message', flat=True).filter(pk=1)[0]
                    }
                ),
                content_type='application/json'
            )

        try:
            codeObj = Codes.objects.get(code__exact=inputCode)
            if codeObj.is_used == True:
                return HttpResponse(
                    json.dumps(
                        {
                            "is_valid": False,
                            "message": Messages.objects.values_list('message', flat=True).filter(pk=3)[0]
                        }
                    ),
                    content_type='application/json'
                )

            return HttpResponse(
                json.dumps(
                    {
                        "is_valid": False,
                        "message": Messages.objects.values_list('message', flat=True).filter(pk=2)[0]
                    }
                ),
                content_type='application/json'
            )
        except ObjectDoesNotExist:
            return HttpResponse(
                json.dumps(
                    {
                        "is_valid": False,
                        "message": Messages.objects.values_list('message', flat=True).filter(pk=1)[0]
                    }
                ),
                content_type='application/json'
            )
    return HttpResponse(
        json.dumps(
            {
                "is_valid": False,
                "message": Messages.objects.values_list('message', flat=True).filter(pk=1)[0]
            }
        ),
        content_type='application/json'
    )


@shared_task
def send_mail(request):
    if request.method == "POST" and request.POST.get('inputEmail') and request.POST.get('textQuestion'):
        contact_email = request.POST.get('inputEmail')
        form_content = request.POST.get('textQuestion')
        #print(contact_email + ' ' + form_content)
        template = loader.get_template('contact_template.txt')

        context = {
            'contact_email': contact_email,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "Новое сообщение с обратной связи Lactonia",
            content,
            "From Lactonia Promo",
            ['promolactonia@gmail.com'],
            headers={'Reply-To': contact_email}
        )

        email.send()
    return HttpResponseRedirect('/registration')
