# Create your views here.
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from .models import *

def home(request):
    today = datetime.date.today()
    window = today-datetime.timedelta(days=7)
    yesterday = today-datetime.timedelta(days=1)
    try:
        current = DietDay.objects.filter(date=datetime.datetime.now())[0]
    except IndexError:
        add_day = DietDay(date=datetime.datetime.now(),calories=0)
        add_day.save()
        
    days = DietDay.objects.exclude(date__lt=window).order_by('-date')
    bank = CalorieBank.objects.all()[0]
    
    ctx = {
        "bank":bank,
        "days":days,
        "today":today,
        "yesterday":yesterday
        }

    return render_to_response("index.html", ctx, RequestContext(request))
    
def update_calories(request):
    day_id = request.GET.get('day_id')
    cals = request.GET.get('calories')
    day = DietDay.objects.get(id=day_id)
    day.calories = cals
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
        "balance": balance
    }
    
    data = simplejson.dumps(sent_data)
    return HttpResponse(data, mimetype='application/json')
