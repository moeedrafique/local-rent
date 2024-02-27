from django.urls import path

from . import views
from .views import *

app_name = 'web'

urlpatterns = [
    ############## CARS ###################
    path('', views.dash, name='home'),
    path('filter/', views.filter, name='filter'),
    path('find-cars/', views.showCars, name='show_cars'),
    # path('car_list/', car_list, name='car_list'),
    # path('car_list/<int:city_id>/', views.car_list, name='car_list_city'),

    path('get_available_cars/', get_available_cars, name='get_available_cars'),

    path('about-us/', about, name='about'),
    path('contact-us/', contact_us, name='contact_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', terms, name='terms'),
    path('cars/', car_details, name='car_details'),
    path('api/bookings/', create_booking, name='create_booking'),
    path('delivery_options/', views.delivery_options, name='delivery_options'),
    path('create_payment_intent/', create_payment_intent, name='create_payment_intent'),

]