from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return "{name: %s}" % self.name

class Drug(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return "{name: %s}" % self.name

class Recipe(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='recipeDoctor')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    drugs = models.ManyToManyField(Drug, related_name='drugs')
    
    def __str__(self):
        return "{doctor: %s, user: %s, drugs: %s}" % (self.doctor, self.user, self.drugs)

