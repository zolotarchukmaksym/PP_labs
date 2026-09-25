from rest_framework import viewsets
from .models import Customer, Technician, Repair, Part, Feedback, RepairStatus
from .serializers import CustomerSerializer, TechnicianSerializer, RepairSerializer, PartSerializer, FeedbackSerializer, RepairStatusSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer

class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer

    @action(detail=False, methods=['get'])
    def report(self, request):
        data = Repair.objects.values('status').annotate(count=models.Count('id'))
        return Response(data)

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class RepairStatusViewSet(viewsets.ModelViewSet):
    queryset = RepairStatus.objects.all()
    serializer_class = RepairStatusSerializer