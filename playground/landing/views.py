from django.shortcuts import render
from django.http import HttpResponse 
from datetime import date

# Create your views here.
def home(request):
    today  = date.today
    stack = [{'id':'python', 'name':'Pyhton'}, {'id':'django', 'name':'Django'}, {'id':'matlab', 'name':'MATLAB'}]
    return render(request, "landing/landing.html", 
                  {"name": "Ricardo", 
                   "today": today,
                   "age": 25,
                   "stack": stack
                   })

def stack_detail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")