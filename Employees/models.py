from django.db import models
from Manager.models import Employee
from django.urls import reverse
# Create your models here.
class Tip(models.Model):
    date = models.DateField()
    tip_amount = models.FloatField()
    time_frame = models.CharField(max_length = 20, choices = (('AM','AM'),('PM','PM')), null=True, blank=True)
    paid_today = models.FloatField()
    paid_later = models.FloatField()
    point = models.FloatField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    

class Form(models.Model):
    date = models.DateField()
    time = models.TimeField()
    time_frame = models.CharField(max_length = 20, choices = (('AM','AM'),('PM','PM')))
    submitted_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cc_tip = models.FloatField()
    service_charge = models.FloatField()
    cash_sales = models.FloatField()
    cash_tip = models.FloatField()
    pre_shift_tip = models.FloatField()

    def get_absolute_url(self):
        return reverse('update_form', kwargs={'id':self.id})
