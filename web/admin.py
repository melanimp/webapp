from django.contrib import admin
from django.contrib.auth.models import User, Group
from web.models import *
# Register your models here.

admin.site.register([ Rol, Type, Usuario, Actividad, Evidence])
admin.site.unregister([User, Group])