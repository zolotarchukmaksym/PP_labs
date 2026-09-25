from django.contrib import admin
from .models import Customer, Device, Repair, RepairStatus, CustomerFeedback, Payment, Part, PartRepair, Technician, TechnicianRepair


admin.site.site_header = 'Repair Application'
admin.site.register(Customer)
admin.site.register(Device)
admin.site.register(Repair)
admin.site.register(RepairStatus)
admin.site.register(CustomerFeedback)
admin.site.register(Payment)
admin.site.register(Part)
admin.site.register(PartRepair)
admin.site.register(Technician)
admin.site.register(TechnicianRepair)