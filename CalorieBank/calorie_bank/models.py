#from django.core.signals import request_finished
import datetime

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models

# Create your models here.
class DietDay(models.Model):
    date = models.DateField()
    calories = models.IntegerField()
    
    def save(self):
        bank = CalorieBank.objects.all()[0]        
        super(DietDay,self).save()
        bank.save()
    
    def __unicode__(self):
        return "%s (%s)" % (self.date, self.calories)

@receiver(post_delete)
def update_bank(sender, **kwargs):
    bank = CalorieBank.objects.all()[0]
    bank.save()

post_delete.connect(update_bank, sender=DietDay)

class CalorieBank(models.Model):
    balance = models.IntegerField()
    updated = models.DateTimeField()
    max_balance = models.IntegerField()

    def save(self):
        bal = 0
        days = DietDay.objects.all().exclude(date=datetime.datetime.now())
        today = DietDay.objects.all().filter(date=datetime.datetime.now())[0]
        for day in days:
            remainder = settings.MAX_DAILY_CALS-day.calories
            if remainder > settings.MAX_BANKED_CALS:
                remainder = settings.MAX_BANKED_CALS
            bal += remainder
        if today.calories>settings.MAX_DAILY_CALS:
            bal = bal-(today.calories-settings.MAX_DAILY_CALS)
        self.balance=bal
        print bal
        super(CalorieBank,self).save()

    def __unicode__(self):
        return "%s" % self.balance
