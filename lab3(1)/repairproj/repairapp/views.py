from rest_framework import viewsets

from .models import CustomerFeedback, Payment, Part, PartRepair, Technician, TechnicianRepair
from .repository import Repository
from .serializer import (
    CustomerSerializer, DeviceSerializer, RepairStatusSerializer, RepairSerializer,
    CustomerFeedbackSerializer, PaymentSerializer, PartSerializer, PartRepairSerializer,
    TechnicianSerializer, TechnicianRepairSerializer
)

repository = Repository()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = repository.get_all_customers()
    serializer_class = CustomerSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = repository.get_all_devices()
    serializer_class = DeviceSerializer

class RepairStatusViewSet(viewsets.ModelViewSet):
    queryset = repository.get_all_repair_statuses()
    serializer_class = RepairStatusSerializer

class RepairViewSet(viewsets.ModelViewSet):
    queryset = repository.get_all_repairs()
    serializer_class = RepairSerializer

class CustomerFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CustomerFeedback.objects.all()
    serializer_class = CustomerFeedbackSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartRepairViewSet(viewsets.ModelViewSet):
    queryset = PartRepair.objects.all()
    serializer_class = PartRepairSerializer

class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer

class TechnicianRepairViewSet(viewsets.ModelViewSet):
    queryset = TechnicianRepair.objects.all()
    serializer_class = TechnicianRepairSerializer
