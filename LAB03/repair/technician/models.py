from django.db import models

class Technician(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    class Meta:
        db_table = 'technician'

    def __str__(self):
        return self.name