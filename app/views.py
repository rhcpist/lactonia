import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from .tasks import send_sms

from .models import Blocklist
from .models import Codes
from .models import Users
from .models import Messages


def index(request):
    return render(request, 'index.html', {'question': 'Hello'})


def win(request):
    template = loader.get_template('win.html')
    context = {
        'param': 'Hello',
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
        # send_sms('380636994338')

        inputName = str(request.POST.get('inputname'))
        birthDate = str(request.POST.get('birthdate'))
        phoneNumber = str(request.POST.get('phone'))
        city = str(request.POST.get('city'))
        inputCode = str(request.POST.get('code'))

        try:
            codeObj = Codes.objects.get(code__exact=inputCode, is_used__exact=False)
            userModel = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=codeObj)
            codeObj.is_used = True
            userModel.code = codeObj
            userModel.status = Messages.objects.get(id__exact=2)
            userModel.save()
            codeObj.user = userModel
            codeObj.save()

        except ObjectDoesNotExist:
            userModel = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=None)
            try:
                blockList = Blocklist.objects.get(phone_number__exact=phoneNumber)
                if blockList.is_block == True:
                    if blockList.date_block <= datetime.now() - timedelta(days=1):
                        blockList.is_block = False
                    return render(request, 'registration.html', {'question': 'Hello'})
                elif blockList.count == 5:
                    blockList.count = 0
                    blockList.date_block = datetime.now()
                    blockList.is_block = True
                    userModel = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=None)
                    userModel.status = Messages.objects.get(id__exact=4)
                    userModel.save()
                else:
                    blockList.date_block = datetime.now()
                    blockList.count += 1
                    userModel = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=None)
                    userModel.status = Messages.objects.get(id__exact=1)
                    userModel.save()
            except ObjectDoesNotExist:
                userModel = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=None)
                userModel.status = Messages.objects.get(id__exact=1)
                userModel.save()
                blockList = Blocklist(phone_number=phoneNumber, count=1)
            blockList.user = userModel
            blockList.save()
    return render(request, 'registration.html', {'question': 'Hello'})


@csrf_exempt
def send_code(request):
    if request.method == "POST":
        inputCode = str(request.POST.get('code'))
        if len(inputCode) == 9:
            try:
                codeObj = Codes.objects.get(code__exact=inputCode)
                if codeObj.is_used == False:
                    return HttpResponse(json.dumps({"is_valid": True,
                                                    "message": Messages.objects.values_list('message', flat=True).filter(pk=2)[0]}),
                                        content_type='application/json')
                else:
                    # try:
                    #     blockList = Blocklist.objects.get(is_block__exact=True)
                    # except ObjectDoesNotExist:
                    #     pass
                    return HttpResponse(json.dumps(
                        {"is_valid": False, "message": Messages.objects.values_list('message', flat=True).filter(pk=3)[0]}),
                                        content_type='application/json')
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({"is_valid": False,
                                                "message": Messages.objects.values_list('message', flat=True).filter(pk=1)[0]}),
                                    content_type='application/json')