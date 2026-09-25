from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, DeviceViewSet, RepairStatusViewSet, RepairViewSet,
    CustomerFeedbackViewSet, PaymentViewSet, PartViewSet, PartRepairViewSet,
    TechnicianViewSet, TechnicianRepairViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'repair-statuses', RepairStatusViewSet)
router.register(r'repairs', RepairViewSet)
router.register(r'customer-feedbacks', CustomerFeedbackViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'parts', PartViewSet)
router.register(r'part-repairs', PartRepairViewSet)
router.register(r'technicians', TechnicianViewSet)
router.register(r'technician-repairs', TechnicianRepairViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
