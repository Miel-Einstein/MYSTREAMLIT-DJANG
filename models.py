#django-bootstrap 4
#django cms


from sys import is_finalizing

from django.contrib.auth.models import User
from django.db import models

# class Site(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='sites')
#     registration_date = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=31)
#     is_active = models.BooleanField(default=True)
#     details = models.CharField(max_length=1023, blank=True, null=True)

#     def __str__(self):
#         return f"{self.name}"


class Address(models.Model):
    class Meta:
        verbose_name_plural = 'addresses'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_address',null=True)
    street = models.CharField(max_length=31)
    street_number = models.CharField(max_length=7, blank=True, null=True)
    city = models.CharField(max_length=31)
    province = models.CharField(max_length=7)
    region = models.CharField(max_length=31, blank=True, null=True)
    country = models.CharField(max_length=31)
    postal_code = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    details = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return f"{self.street} {self.street_number}, {self.city} ({self.province}), {self.region}, {self.country}, {self.postal_code}"


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=6)
    details = models.CharField(max_length=1023, blank=True, null=True)
    attached_time=models.DateTimeField(null=True)
    dettached_time=models.DateTimeField(null=True)
    # maybe manage in logs record 

    def __str__(self):
        return self.id

class Tree(models.Model):
    id = models.AutoField(primary_key=True)

    picture=models.ImageField(upload_to='static/tree_images/')
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description=models.TextField(blank=True,null=True)
    tree_treshold_pending=models.FloatField() # verify if better on device (retalk)
    #Add trees typeand name from csv or api t integrate as choice 
    def __str__(self):
        return f"Image for {self.id}"

class Alert(models.Model):
    class AlertStatus(models.TextChoices):
        Urgent = 'Yes', 'Yes'
        Mid_Urgent = 'No', 'No'
    alert_status= models.CharField(
        max_length=3,
        choices=AlertStatus.choices,
        default=AlertStatus.Urgent,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_message')  # 
        
    message=models.TextField()

class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_notification')
        
    message=models.TextField()   
class Tocs(Device):
    class BatteryStatus(models.TextChoices):
        OFF = 'OFF', 'Off'
        ON = 'ON', 'On'
        LOW = 'LOW', 'Low'
    mac_address = models.CharField(max_length=18,null=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='tocs_user',null=True)
        
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0) # use tocs logs instead of latitude or longitude  
    tree=models.ManyToManyField(Tree,  related_name='tree')
    battery_status = models.CharField(
        max_length=3,
        choices=BatteryStatus.choices,
        default=BatteryStatus.OFF,
    )
    # for admin only
    treshold=models.FloatField(blank=True,null=True)
    def __str__(self):
        return self.mac_address


# Data
# un evento è un CSV
# CSV Che hanno duration<1 min non vanno scaricati
class TocsEvent(models.Model):
    id = models.AutoField(primary_key=True)
    tocs = models.ForeignKey(
        Tocs, on_delete=models.CASCADE, related_name='events')
    csv_path = models.FilePathField()
    start = models.DateTimeField()
    duration = models.DateTimeField()
    ax_mean = models.FloatField()
    ay_mean = models.FloatField()
    az_mean = models.FloatField()
    ax_std = models.FloatField()
    ay_std = models.FloatField()
    az_std = models.FloatField()
    ax_peak = models.FloatField()
    ay_peak = models.FloatField()
    az_peak = models.FloatField()

    def __str__(self):
        return self.id


# Note the row is filled with resampled data
# Use linear interpolation to resample
# Check MADE code
class TocsCSVRow(models.Model):
    # id = models.AutoField(primary_key=True)
    sensor_id=models.CharField(max_length=200,null=True)
    tocs=models.ForeignKey(Tocs,on_delete=models.DO_NOTHING,related_name='csv_tocs',null=True)
    # events = models.ForeignKey(
    #     TocsEvent, on_delete=models.CASCADE, related_name='csv_rows')
    time = models.DateTimeField()
    ax = models.FloatField()
    ay = models.FloatField()
    az = models.FloatField()
    temp = models.FloatField()

    def __str__(self):
        return self.sensor_id

