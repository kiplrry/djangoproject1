from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='todos',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Todo<{self.id}> completed:{self.completed}'
    
    class Meta:
        ordering = ['-created', '-updated']
