from django.http import HttpResponse
from django.template import loader
from .models import Blocklist
from .models import Codes
from .models import Users


def index(request):
    template = loader.get_template('index.html')
    context = {
        'param': 'Hello',
    }
    return HttpResponse(template.render(context, request))

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
    template = loader.get_template('registration.html')
    context = {
        'param': 'Hello',
    }
    return HttpResponse(template.render(context, request))