# Create your views here.
import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import *

def home(request):
    today = datetime.date.today()
    window = today-datetime.timedelta(days=7)
    days = DietDay.objects.exclude(date__lt=window).order_by('-date')
    bank = CalorieBank.objects.all()[0]
    
    ctx = {
        "bank":bank,
        "days":days,
        "today":today
        }

    return render_to_response("index.html", ctx, RequestContext(request))
