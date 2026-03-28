from django.db import models

class PatientAnalysis(models.Model):
    summary = models.TextField()
    diagnosis = models.CharField(max_length=255)
    reasoning = models.TextField()
    confidence = models.CharField(max_length=20)
    risk_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diagnosis