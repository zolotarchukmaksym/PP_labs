from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Customer'

class Device(models.Model):
    CATEGORY_CHOICES = [
        ('phone', 'Phone'),
        ('laptop', 'Laptop'),
        ('tablet', 'Tablet'),
        ('other', 'Other')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='devices')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.category} - {self.model}"

    class Meta:
        db_table = 'Device'

class Repair(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='repairs')
    technician = models.ForeignKey('Technician', on_delete=models.SET_NULL, null=True, related_name='repairs')
    repair_time = models.TimeField()
    repair_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('RepairStatus', on_delete=models.SET_NULL, null=True, related_name='repairs')
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repair for {self.device} by {self.technician} on {self.repair_date}"

    class Meta:
        db_table = 'Repair'

class RepairStatus(models.Model):
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_name

    class Meta:
        db_table = 'RepairStatus'

class Technician(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Technician'

class Feedback(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, related_name='feedbacks')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks')
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Оцінка від 1 до 5
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback for {self.repair} by {self.customer}"

    class Meta:
        db_table = 'Feedback'