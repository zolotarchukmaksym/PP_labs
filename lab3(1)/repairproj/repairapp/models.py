from django.db import models

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Surname = models.CharField(max_length=50, unique=True)
    Address = models.TextField(blank=True, null=True)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    PhoneNumber = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.Name} {self.Surname}"

class Technician(models.Model):
    TechnicianID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Surname = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50, blank=True, null=True)
    Specialization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.Name} {self.Surname}"

class Device(models.Model):
    DeviceID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Зовнішній ключ
    DeviceType = models.CharField(max_length=50)
    Model = models.CharField(max_length=100, blank=True, null=True)
    SerialNumber = models.CharField(max_length=50, unique=True, blank=True, null=True)
    Brand = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.DeviceType} - {self.Model}"

class RepairStatus(models.Model):
    RepairStatusID = models.AutoField(primary_key=True)
    StatusName = models.CharField(max_length=50)

    def __str__(self):
        return self.StatusName

class Repair(models.Model):
    RepairID = models.AutoField(primary_key=True)
    DeviceID = models.ForeignKey(Device, on_delete=models.CASCADE)  # Зовнішній ключ
    RepairStatusID = models.ForeignKey(RepairStatus, on_delete=models.CASCADE)  # Зовнішній ключ
    ReceivedDate = models.DateField()
    CompletedDate = models.DateField(blank=True, null=True)
    DescriptionProblem = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Repair ID: {self.RepairID} - Status: {self.RepairStatusID.StatusName}"

class CustomerFeedback(models.Model):
    FeedbackID = models.AutoField(primary_key=True)
    FeedbackDate = models.DateField(auto_now_add=True)
    Rating = models.IntegerField(blank=True, null=True)
    Comment = models.TextField(blank=True, null=True)
    RepairID = models.ForeignKey(Repair, on_delete=models.CASCADE, blank=True, null=True)  # Зовнішній ключ

    def __str__(self):
        return f"Feedback ID: {self.FeedbackID} - Rating: {self.Rating}"

class Payment(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    RepairID = models.ForeignKey(Repair, on_delete=models.CASCADE, blank=True, null=True)  # Зовнішній ключ
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentDate = models.DateField(blank=True, null=True)
    PaymentMethod = models.CharField(max_length=50, blank=True, null=True)
    Cost = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return f"Payment ID: {self.PaymentID} - Amount: {self.Amount}"

class Part(models.Model):
    PartID = models.AutoField(primary_key=True)
    PartName = models.CharField(max_length=50)
    Description = models.TextField(blank=True, null=True)
    Price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return self.PartName

class PartRepair(models.Model):
    PartRepairID = models.AutoField(primary_key=True)
    PartID = models.ForeignKey(Part, on_delete=models.CASCADE)  # Зовнішній ключ
    RepairID = models.ForeignKey(Repair, on_delete=models.CASCADE)  # Зовнішній ключ

    def __str__(self):
        return f"PartRepair ID: {self.PartRepairID}"

class TechnicianRepair(models.Model):
    TechnicianRepairID = models.AutoField(primary_key=True)
    TechnicianID = models.ForeignKey(Technician, on_delete=models.CASCADE)  # Зовнішній ключ
    RepairID = models.ForeignKey(Repair, on_delete=models.CASCADE)  # Зовнішній ключ

    def __str__(self):
        return f"TechnicianRepair ID: {self.TechnicianRepairID}"