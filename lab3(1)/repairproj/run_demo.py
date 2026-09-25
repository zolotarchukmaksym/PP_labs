import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repair.settings')

django.setup()

from repair_app.models import Customer, Technician, Repair
from repair_app.repository import RepositoryFactory

def demo():
    customer_repo = RepositoryFactory.get_repository('customer')
    technician_repo = RepositoryFactory.get_repository('technician')
    repair_repo = RepositoryFactory.get_repository('repair')

    new_customer = Customer(name="Alice Cooper", email="alice@example.com", phone="9876543210")
    new_customer = customer_repo.save(new_customer)
    print(f"Added customer: {new_customer.name}")

    new_technician = Technician(name="Bob Marley", specialization="Laptop Repair")
    new_technician = technician_repo.save(new_technician)
    print(f"Added technician: {new_technician.name}")

    new_repair = Repair(customer=new_customer, technician=new_technician, device="Laptop", status="In Progress", issue="Broken screen")
    new_repair = repair_repo.save(new_repair)
    print(f"Added repair: {new_repair.device} by {new_repair.technician.name}")

    all_customers = customer_repo.get_all()
    print("\nAll customers:")
    for customer in all_customers:
        print(f"{customer.name}, {customer.email}, {customer.phone}")

    all_technicians = technician_repo.get_all()
    print("\nAll technicians:")
    for technician in all_technicians:
        print(f"{technician.name}, {technician.specialization}")

    all_repairs = repair_repo.get_all()
    print("\nAll repairs:")
    for repair in all_repairs:
        print(f"Repair for {repair.device} by {repair.technician.name}, Status: {repair.status}, Issue: {repair.issue}")

if __name__ == "__main__":
    demo()
