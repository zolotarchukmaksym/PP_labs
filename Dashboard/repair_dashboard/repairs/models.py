from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Technician(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Device(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='devices')
    device_type = models.CharField(max_length=100)  # Наприклад: телефон, ноутбук
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.serial_number})"


class Repair(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='repairs')
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    issue_description = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('awaiting_parts', 'Awaiting Parts')
    ])
    repair_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Repair for {self.device} by {self.technician} - Status: {self.status}"


class Part(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='parts')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"


class Feedback(models.Model):
    repair = models.OneToOneField(Repair, on_delete=models.CASCADE, related_name='feedback')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Оцінка від 1 до 5
    comment = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.customer} - Rating: {self.rating}"