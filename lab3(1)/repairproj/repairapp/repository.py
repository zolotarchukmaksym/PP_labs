from .models import (
    Customer,
    Device,
    RepairStatus,
    Repair,
    CustomerFeedback,
    Payment,
    Part,
    Technician,
    PartRepair,
    TechnicianRepair,
)

class BaseRepository:
    model = None  # Має бути визначено в підкласах

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, instance_id):
        return self.model.objects.filter(id=instance_id).first()

    def add(self, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance

    def update(self, instance_id, **kwargs):
        instance = self.get_by_id(instance_id)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    def delete(self, instance_id):
        instance = self.get_by_id(instance_id)
        if instance:
            instance.delete()
            return True
        return False


class CustomerRepository(BaseRepository):
    model = Customer


class DeviceRepository(BaseRepository):
    model = Device

class RepairStatusRepository(BaseRepository):
    model = RepairStatus

class RepairRepository(BaseRepository):
    model = Repair


class CustomerFeedbackRepository(BaseRepository):
    model = CustomerFeedback


class PaymentRepository(BaseRepository):
    model = Payment


class PartRepository(BaseRepository):
    model = Part


class TechnicianRepository(BaseRepository):
    model = Technician


class PartRepairRepository(BaseRepository):
    model = PartRepair


class TechnicianRepairRepository(BaseRepository):
    model = TechnicianRepair


# Менеджер для всіх репозиторіїв
class RepositoryManager:
    def __init__(self):
        self.repos = {
            'customer': CustomerRepository(),
            'device': DeviceRepository(),
            'repair_status': RepairStatusRepository(),
            'repair': RepairRepository(),
            'customer_feedback': CustomerFeedbackRepository(),
            'payment': PaymentRepository(),
            'part': PartRepository(),
            'technician': TechnicianRepository(),
            'part_repair': PartRepairRepository(),
            'technician_repair': TechnicianRepairRepository(),
        }