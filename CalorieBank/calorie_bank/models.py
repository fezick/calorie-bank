from django.db import models

# Create your models here.
class DietDay(models.Model):
    date = models.DateTimeField()
    calories = models.IntegerField()
    
    def save(self):
        bank = CalorieBank.objects.all()[0]
        bank.save()
        super(DietDay,self).save()
    
    def __unicode__(self):
        return "%s (%s)" % (self.date, self.calories)

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
        super(CalorieBank,self).save()

    def __unicode__(self):
        return "%s" % self.balance
