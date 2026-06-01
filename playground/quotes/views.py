from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

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
    list_items = ""
    days = list(days_of_week.keys())
    for day in days:
        day_path =  reverse("day-quote", args = [day])
        list_items+= f"<li><a href= '{day_path}'>{day}</a></li>"
    response_html = f"<ul>{list_items}</ul>"
    return HttpResponse(response_html)

def days_week(request, day):
    try:
        quote_text = days_of_week[day]
        return HttpResponse(quote_text)
    except:
        return HttpResponseNotFound("No hay frase para este día")
    
def days_week_num(request, day):
    days = list(days_of_week.keys())
    if day > len(days) or day == 0:
        return HttpResponseNotFound("El día no existe")
    redirect_day = days[day-1]
    redirect_path = reverse("day-quote", args = [redirect_day])
    return HttpResponseRedirect(redirect_path)