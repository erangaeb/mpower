from django.db import models
from django.contrib.auth.models import User


class Power(models.Model):
    voltage = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                  blank=True, default=None)
    current = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                  blank=True, default=None)
    frequency = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                                    blank=True, default=None)
    kwh = models.DecimalField(max_digits=10, decimal_places=5, null=True,
                              blank=True, default=None)
    user = models.ForeignKey(User)
