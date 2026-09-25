from django.contrib import admin
from .models import Customer, Technician, Repair, Part, Feedback, RepairStatus

admin.site.register(Customer)
admin.site.register(Technician)
admin.site.register(Repair)
admin.site.register(Part)
admin.site.register(Feedback)
admin.site.register(RepairStatus)