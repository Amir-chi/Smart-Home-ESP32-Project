from django.contrib import admin

from .models import Esp32Picture , CommandHistory , LedStatus



admin.site.register(Esp32Picture)
admin.site.register(CommandHistory)
admin.site.register(LedStatus)