from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, default='postgres')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
