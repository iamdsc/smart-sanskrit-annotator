#django-admin.py is Django’s command-line utility for administrative tasks

from django.contrib import admin
from .models import Sentences,linetypes,WordOptions,Wordsinsentence


admin.site.register(Sentences)
admin.site.register(Wordsinsentence)
admin.site.register(WordOptions)
admin.site.register(linetypes)

