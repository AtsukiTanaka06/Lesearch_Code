from django.db import models

# Create your models here.
class ColumnSettings(models.Model):
    title = models.CharField(max_length=100)
    platform = models.BinaryField(null=True)
    customer = models.BinaryField(null=True)
    survey = models.BinaryField(null=True)
    menu = models.BinaryField(null=True)
    channel = models.BinaryField(null=True)
    conversion = models.BinaryField(null=True)


