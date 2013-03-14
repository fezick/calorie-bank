# Create your views here.
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from .models import *

def home(request):
    today = datetime.date.today()
    window = today-datetime.timedelta(days=31)
    # get all the diet day objects 
    days = DietDay.objects.exclude(date__lt=window).order_by('-date')
    
    # check for missing days by comparing today's date with the last date 
    # in the set. If there are missing dates, create them.
    last_day = days[0]
    delta = (today-last_day.date).days # get time diff
    day_shift = delta-1 # offset by one to make sure today gets created
    while day_shift >= 0:
        new_date = datetime.date.today() - datetime.timedelta(days=day_shift)
        try:
            check_day = DietDay.objects.get(date=new_date)
        except DietDay.DoesNotExist:
            add_day = DietDay(date=new_date,calories=0)
            add_day.save()
        day_shift=day_shift-1
        
    bank = CalorieBank.objects.all()[0]
    
    for d in days:
        balance = settings.MAX_DAILY_CALS-d.calories
        if balance > settings.MAX_BANKED_CALS:
            balance = settings.MAX_BANKED_CALS
        d.balance = balance

    ctx = {
        "bank":bank,
        "days":days,
        "today":today,
        }

    return render_to_response("index.html", ctx, RequestContext(request))
    
def update_calories(request):
    day_id = request.GET.get('day_id')
    cals = request.GET.get('calories')
    day = DietDay.objects.get(id=day_id)
    day.calories = cals
    day_bal = settings.MAX_DAILY_CALS-float(cals)
    if day_bal > settings.MAX_BANKED_CALS:
        day_bal = settings.MAX_BANKED_CALS
    try:
        day.save()
    except:
        return HttpResponse("false")
    updated_day = DietDay.objects.get(id=day_id)
    balance = CalorieBank.objects.all()[0].balance
    row_id = "day_%s" % updated_day.id
    sent_data = {
        "cals":updated_day.calories,
        "row_id":row_id,
        "balance": balance,
        "day_bal": day_bal
    }
    
    data = simplejson.dumps(sent_data)
    return HttpResponse(data, mimetype='application/json')
