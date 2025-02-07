from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # Task title (short description)
    title = models.CharField(max_length=100)

    # Detailed description of the task
    description = models.TextField()

    # Due date for the task
    due_date = models.DateField()

    # Status of the task: Pending, In Progress, Completed
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Add a foreign key to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
