# admin.py

from django.contrib import admin
from .models import Customer, Device, Repair, RepairStatus, Technician, Feedback

admin.site.register(Customer)
admin.site.register(Device)
admin.site.register(Repair)
admin.site.register(RepairStatus)
admin.site.register(Technician)
admin.site.register(Feedback)
