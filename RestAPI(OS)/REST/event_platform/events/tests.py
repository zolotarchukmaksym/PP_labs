from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, EventLocation, EventOrganizer, Event, Ticket, Registration

class EventModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name="Technology", description="Tech-related events")
        self.location = EventLocation.objects.create(name="Tech Venue", address="123 Tech Street", contact_email="info@techvenue.com")
        self.organizer = EventOrganizer.objects.create(user=self.user, company_name="Tech Corp", bio="Organizing tech events.")
        self.event = Event.objects.create(
            name="Tech Conference 2024",
            description="A large technology conference.",
            start_date="2024-12-01T09:00:00Z",
            end_date="2024-12-01T18:00:00Z",
            location=self.location,
            category=self.category,
            organizer=self.organizer
        )
        self.ticket = Ticket.objects.create(event=self.event, ticket_type="VIP", price=100.00, quantity_available=50)
        self.registration = Registration.objects.create(event=self.event, user=self.user, ticket=self.ticket)

    def test_event_creation(self):
        event = self.event
        self.assertEqual(event.name, "Tech Conference 2024")
        self.assertEqual(event.location.name, "Tech Venue")
        self.assertEqual(event.category.name, "Technology")

    def test_ticket_creation(self):
        ticket = self.ticket
        self.assertEqual(ticket.ticket_type, "VIP")
        self.assertEqual(ticket.price, 100.00)

    def test_registration_creation(self):
        registration = self.registration
        self.assertEqual(registration.user.username, "testuser")
        self.assertEqual(registration.event.name, "Tech Conference 2024")

    def test_event_list_view(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Conference 2024")
