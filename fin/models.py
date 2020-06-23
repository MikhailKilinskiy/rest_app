from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Cost(models.Model):
    name = models.CharField(max_length=250)
    amount = models.FloatField()
    date = models.DateField()
    create_date = models.DateTimeField(default=now, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "Cost name: "+str(self.name)