#from django.core.signals import request_finished
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
    
    """def delete():
        bank = CalorieBank.objects.all()[0]        
        super(delete,self).delete()
        bank.save()"""
    
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
        days = DietDay.objects.all()
        for day in days:
            remainder = 2000-day.calories
            if remainder > 200:
                remainder = 200
            bal += remainder
        self.balance=bal
        print bal
        super(CalorieBank,self).save()

    def __unicode__(self):
        return "%s" % self.balance
