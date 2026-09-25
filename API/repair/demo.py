import os
import django

# Встановлюємо змінну середовища DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repair.settings')  # Замість 'repair_app.settings' використовуйте шлях до ваших налаштувань

# Ініціалізація Django
django.setup()

# Імпортуємо ваш репозиторій
from repair_app.repository import RepositoryFactory

from repair_app.models import Customer, Technician, Repair  # Імпорт моделей
from repair_app.repository import RepositoryFactory


def demo():
    # Демо для роботи з Customer
    customer_repo = RepositoryFactory.get_repository('customer')

    # Додати нового клієнта
    new_customer = customer_repo.save(Customer(name="John Doe", email="john@example.com", phone="1234567890"))
    print(f"Added customer: {new_customer}")

    # Вичитати всіх клієнтів
    all_customers = customer_repo.get_all()
    print("All customers:")
    for customer in all_customers:
        print(customer)

    # Демо для роботи з Technician
    technician_repo = RepositoryFactory.get_repository('technician')

    # Додати нового техніка
    new_technician = technician_repo.save(Technician(name="Jane Smith", specialization="Electronics"))
    print(f"Added technician: {new_technician}")

    # Вичитати всіх техніків
    all_technicians = technician_repo.get_all()
    print("All technicians:")
    for technician in all_technicians:
        print(technician)

    # Демо для роботи з Repair
    repair_repo = RepositoryFactory.get_repository('repair')

    # Додати новий ремонт
    new_repair = repair_repo.save(
        Repair(device="Laptop", issue="Broken screen", technician=new_technician, customer=new_customer))
    print(f"Added repair: {new_repair}")

    # Вичитати всі ремонти
    all_repairs = repair_repo.get_all()
    print("All repairs:")
    for repair in all_repairs:
        print(repair)


if __name__ == "__main__":
    demo()