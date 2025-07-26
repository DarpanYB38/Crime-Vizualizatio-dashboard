from django.db import models

# Create your models here.

class CrimeRecord(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=255)
    crime_type = models.CharField(max_length=100)
    modus_operandi = models.TextField()
    weapon_used = models.CharField(max_length=100)
    description = models.TextField()
    case_status = models.CharField(max_length=50)  # Solved or Pending
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    punishment = models.TextField(null=True, blank=True)
    Indian_Penal_Code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.crime_type} - {self.location} ({self.date})"

class CrimePrediction(models.Model):
    location = models.CharField(max_length=100)
    modus_operandi = models.CharField(max_length=100)
    weapon_used = models.CharField(max_length=100)
    predicted_crime_type = models.CharField(max_length=100)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.predicted_crime_type} ({self.confidence}%)"
