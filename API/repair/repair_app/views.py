from .repository import RepositoryFactory

def demonstrate_repository_usage():
    # Демонстрація використання репозиторіїв

    # Додати новий Customer
    customer_repo = RepositoryFactory.get_repository('customer')
    new_customer = customer_repo.save(customer_repo.model(name='John Doe', email='john@example.com', phone='123456789'))
    print(f"Added Customer: {new_customer}")

    # Додати новий Technician
    technician_repo = RepositoryFactory.get_repository('technician')
    new_technician = technician_repo.save(technician_repo.model(name='Jane Smith', specialization='Electronics'))
    print(f"Added Technician: {new_technician}")

    # Отримати всі Repairs
    repair_repo = RepositoryFactory.get_repository('repair')
    repairs = repair_repo.get_all()
    print("All Repairs:")
    for repair in repairs:
        print(repair)

    # Отримати Customer по ID
    customer = customer_repo.get_by_id(new_customer.id)
    print(f"Retrieved Customer: {customer}")
