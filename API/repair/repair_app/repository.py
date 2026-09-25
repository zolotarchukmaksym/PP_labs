from .models import Customer, Technician, Repair, Part, Feedback, RepairStatus

class BaseRepository:
    model = None

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.objects.get(id=id)

    @classmethod
    def save(cls, instance):
        instance.save()
        return instance


class CustomerRepository(BaseRepository):
    model = Customer


class TechnicianRepository(BaseRepository):
    model = Technician


class RepairRepository(BaseRepository):
    model = Repair


class PartRepository(BaseRepository):
    model = Part


class FeedbackRepository(BaseRepository):
    model = Feedback


class RepairStatusRepository(BaseRepository):
    model = RepairStatus


class RepositoryFactory:
    @staticmethod
    def get_repository(entity_name):
        repositories = {
            'customer': CustomerRepository,
            'technician': TechnicianRepository,
            'repair': RepairRepository,
            'part': PartRepository,
            'feedback': FeedbackRepository,
            'repair_status': RepairStatusRepository,
        }
        return repositories.get(entity_name.lower())
