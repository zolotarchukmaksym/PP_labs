from django.test import TestCase
from .repository import Repository
from .models import Customer

class RepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = Repository()
        Customer.objects.create(name="John", surname="Doe", phone_number="123456789", email="john@example.com", address="123 Main St")

    def test_get_all_customers(self):
        customers = self.repo.get_all_customers()
        self.assertEqual(customers.count(), 1)

    def test_create_customer(self):
        customer = self.repo.create_customer("Jane", "Doe", "987654321", "jane@example.com", "456 Main St")
        self.assertEqual(customer.name, "Jane")
        self.assertEqual(customer.surname, "Doe")
