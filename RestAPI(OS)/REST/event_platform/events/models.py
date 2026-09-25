from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class EventLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class EventOrganizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.company_name

class EventSponsor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='sponsors')

    def __str__(self):
        return self.name

class EventSpeaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='speakers')

    def __str__(self):
        return self.name

class EventActivity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='activities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(EventLocation, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100)  # Тип квитка: стандартний, VIP
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ticket_type} - {self.event.name}"

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Рейтинг (1-5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event} ({self.rating}/5)"