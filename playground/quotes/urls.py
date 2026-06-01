from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<int:day>", views.days_week_num),
    path("<str:day>", views.days_week, name = "day-quote")
]
