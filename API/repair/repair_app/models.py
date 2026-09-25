from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Technician(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Repair(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    device = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    repair_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Repair for {self.device} by {self.technician}'


class Part(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.customer}'


class RepairStatus(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    status_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Status for {self.repair}: {self.status}'
