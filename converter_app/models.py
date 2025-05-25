from datetime import timedelta
from django.db import models
from django.utils import timezone

# Create your models here.

class EmailUsers(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Outbox', 'Outbox'),
        ('Failed', 'Failed'),
        ('Sending', 'Sending'),
        ('Scheduled', 'Scheduled'),
    )

    subject = models.CharField(max_length=255)
    body = models.TextField
    email = models.ManyToManyField(EmailUsers)
    Status = models.CharField(max_length=50, choices=EMAIL_STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject




