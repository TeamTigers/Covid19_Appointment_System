from django.contrib import admin
from .models import appointment,posative,neagtive,donor
# Register your models here.
admin.site.register(appointment)
admin.site.register(posative)
admin.site.register(neagtive)
admin.site.register(donor)