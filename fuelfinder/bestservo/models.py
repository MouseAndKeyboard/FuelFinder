from django.db import models

# Create your models here.
class ServiceStations(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=30)
    date = models.DateField()
    price = models.FloatField()
    trading_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    site_features = models.CharField(max_length=300)
