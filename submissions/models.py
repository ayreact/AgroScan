from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class PlantDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    image_prompt = models.TextField(blank=True)
    diagnosis_title = models.CharField(max_length=255)
    health_condition = models.TextField()
    cause = models.TextField(default='No control suggested.')
    disease_signs = models.TextField()
    control_suggestions = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diagnosis_title

class StoredDiagnosis(models.Model):
    name = models.CharField(max_length=30)
    diagnosis_title = models.CharField(max_length=255)
    health_condition = models.TextField()
    cause = models.TextField(default='No control suggested.')
    disease_signs = models.TextField()
    control_suggestions = models.TextField()
    summary = models.TextField()