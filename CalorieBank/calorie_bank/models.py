#from django.core.signals import request_finished
import datetime

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models

class DietDay(models.Model):
    """
    An individual day of your diet. Only one per date, but that has not
    yet been enforced in the code yet.
    
    """
    date = models.DateField()
    calories = models.IntegerField()
    
    # when saving, also update the calorie bank object
    def save(self):
        bank = CalorieBank.objects.all()[0]        
        super(DietDay,self).save()
        bank.save()
    
    def __unicode__(self):
        return "%s (%s)" % (self.date.strftime('%a - %h %d %Y'), self.calories)

@receiver(post_delete)
def update_bank(sender, **kwargs):
    """Update bank balance when saving a single days cals"""
    bank = CalorieBank.objects.all()[0]
    bank.save()

post_delete.connect(update_bank, sender=DietDay)

class CalorieBank(models.Model):
    """
    This is the main bank model. As designed, there should only ever need 
    to be one of these, but if accounts are ever added, then that will change.

    """
    balance = models.IntegerField()
    updated = models.DateTimeField()
    max_balance = models.IntegerField()

    def save(self):
        bal = 0
        # get all days except for today
        days = DietDay.objects.all().exclude(date=datetime.datetime.now())

        # check each day for the difference (+ or -) from the max 
        # allowed per day
        for day in days:
            remainder = settings.MAX_DAILY_CALS-day.calories
            if remainder > settings.MAX_BANKED_CALS:
                remainder = settings.MAX_BANKED_CALS
            bal += remainder
        
        # see if today exists and check to see if we over calories.
        # If so, subtract from the bank
        try:
            today = DietDay.objects.filter(date=datetime.datetime.now())[0]
        except IndexError:
            today = None
        if today and today.calories>settings.MAX_DAILY_CALS:
            bal = bal-(today.calories-settings.MAX_DAILY_CALS)

        # Do not allow negative bank balance
        if bal > 0:
            self.balance=bal
        else:
            self.balance=0

        # Jesus saves, so should you
        super(CalorieBank,self).save()

    def __unicode__(self):
        return "%s" % self.balance
