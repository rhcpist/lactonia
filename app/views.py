import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .tasks import send_sms

from .models import Blocklist
from .models import Codes
from .models import Users

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
        #send_sms('380636994338')

        inputName = str(request.POST.get('inputname'))
        birthDate = str(request.POST.get('birthdate'))
        phoneNumber = str(request.POST.get('phone'))
        city = str(request.POST.get('city'))
        inputCode = str(request.POST.get('code'))

        codeObj = Codes.objects.get(code__exact=inputCode)

        user = Users(name=inputName, birth_date=birthDate, phone_number=phoneNumber, city=city, code=codeObj)
        user.save()

    return render(request, 'registration.html', {'question': 'Hello'})

@csrf_exempt
def send_code(request):
    if request.method == "POST":
        inputCode = str(request.POST.get('code'))
        if len(inputCode) == 9:
            try:
                is_set = Codes.objects.get(code__exact=inputCode)
            except Codes.DoesNotExist:
                is_set = None
            if is_set:
                return HttpResponse(json.dumps({"is_valid": True, "message": "Вітаємо, Ваш код успішно зареєстровано, чекайте на розіграш подарунків.  Дане підтвердження буде надіслане на Ваш номер, якщо Ви його не отримаєте, зверніться за номером гарячої лінії 0800210720"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"is_valid": False, "message": "Невірний формат коду. Перевірте правильність та спробуйте ще раз."}), content_type='application/json')
