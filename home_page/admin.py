from django.contrib import admin
from .models import BusInformation, Route, Map, Stops
# Register your models here.

admin.site.register(BusInformation)
admin.site.register(Route)
admin.site.register(Map)
admin.site.register(Stops)
