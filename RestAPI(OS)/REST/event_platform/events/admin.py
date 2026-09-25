from django.contrib import admin
from .models import Event, Ticket, Registration, Review, Category, EventLocation, EventOrganizer, EventSponsor, EventSpeaker, EventActivity

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Registration)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(EventLocation)
admin.site.register(EventOrganizer)
admin.site.register(EventSponsor)
admin.site.register(EventSpeaker)
admin.site.register(EventActivity)