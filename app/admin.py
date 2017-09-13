from django.contrib import admin
from .models import Blocklist
from .models import Codes
from .models import Users

# Register your models here.
admin.site.register(Blocklist)
admin.site.register(Codes)
admin.site.register(Users)