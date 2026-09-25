from rest_framework import serializers

class RepairAvgCostSerializer(serializers.Serializer):
    device_category = serializers.CharField(source='device__category')
    avg_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

class RepairCountTechnicianSerializer(serializers.Serializer):
    technician_name = serializers.CharField(source='technician__name')
    repair_count = serializers.IntegerField()

class RepairStatusCountSerializer(serializers.Serializer):
    status_name = serializers.CharField(source='status__status_name')
    repair_count = serializers.IntegerField()

class TechnicianAvgRatingSerializer(serializers.Serializer):
    technician_name = serializers.CharField(source='technician__name')
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

class TechnicianFeedbackCountSerializer(serializers.Serializer):
    technician_name = serializers.CharField(source='technician__name')
    feedback_count = serializers.IntegerField()

class RepairAvgTimeSerializer(serializers.Serializer):
    status_name = serializers.CharField(source='status__status_name')
    avg_repair_time = serializers.DurationField()
