from django.db import models

# Create your models here.
class Rules(models.Model):
    high_risk_start = models.IntegerField()
    high_risk_end = models.IntegerField()
    medium_risk_start = models.IntegerField()
    medium_risk_end = models.IntegerField()
    low_risk_start = models.IntegerField()
    low_risk_end = models.IntegerField()

    def _str_(self):
        return self.high_risk_start+' '+self.high_risk_end