from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^win/$', views.win, name='win'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registration/send_code$', views.send_code, name='send_code'),
    url(r'^registration/send_mail$', views.send_mail, name='send_mail'),
]