from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, TechnicianViewSet, RepairViewSet, PartViewSet, FeedbackViewSet, RepairStatusViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'technicians', TechnicianViewSet)
router.register(r'repairs', RepairViewSet)
router.register(r'parts', PartViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'repair-statuses', RepairStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
