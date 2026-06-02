from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from datetime import date

# Para simplificar la lógica orignal:
days_of_week = {
    "monday": "Pienso, luego existo",
    "tuesday": "La vida es un sueño",
    "wednesday": "miércoles",
    "thursday": "jueves",
    "friday": "viernes",
    "saturday": "sábado",
    "sunday": "domingo"

}

# Create your views here.

def index(request):
    days = list(days_of_week.keys())
    return render(request, "quotes/quotes.html", {
        "days": days,
    })

def days_week(request, day):
    try:
        quote_text = days_of_week[day]
        return HttpResponse(quote_text)
    except:
        raise Http404()
    
def days_week_num(request, day):
    days = list(days_of_week.keys())
    if day > len(days) or day == 0:
        return HttpResponseNotFound("El día no existe")
    redirect_day = days[day-1]
    redirect_path = reverse("day-quote", args = [redirect_day])
    return HttpResponseRedirect(redirect_path)