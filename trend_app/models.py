from django.db import models

# Create your models here.

class TrendName(models.Model):
    name =  models.CharField(max_length=100)
    search_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Trend(models.Model):
    name = models.ForeignKey(TrendName, related_name="trends", on_delete=models.CASCADE)
    region = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    interest = models.IntegerField()

    def __str__(self):
        return self.name.name
    

