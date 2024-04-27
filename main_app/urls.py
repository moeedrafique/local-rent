from django.urls import path

from . import views
from .views import *
urlpatterns = [

    path('register/', RentalCompanyRegistrationView.as_view(), name='rental_company_signup'),

    ############## CARS ###################
    path('', views.home, name='home'),
    path('cars/new/', views.addCars, name='add_cars'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('cars/', views.all_cars, name='all_cars'),
    path('bookings/', views.carsList, name='all_bookings'),
    path('api/cars/', cars_api, name='cars_api'),
    path('api/bookings/', views.bookings_api, name='bookings_api'),

    ############## USERS ###################

    ############## AGENTS ###################
    path('agents/', views.Agents, name='agents'),
    path('agents/new/', views.addAgents, name='agents_new'),

    ############## INVOICES ###################


    ############## CUSTOMERS ###################
    path('clients/', views.Customers, name='clients'),
    # path('clients/new/', views.addCustomers, name='clients_new'),

    ############## DELIVERY ###################
    path('delivery/', views.all_delivery, name='delivery'),
    path('get_location_types/<int:city_id>/', get_location_types, name='get_location_types'),
    path('get_delivery_items/<int:city_id>/', get_delivery_items, name='get_delivery_items'),
    path('update_delivery/<int:delivery_id>/', update_delivery, name='update_delivery'),
    path('save_changes/', views.save_changes, name='save_changes'),


    ############## DISCOUNTS AND PRICE RAISES ###################
    path('discounts/', views.Discounts, name='discounts'),
    path('discounts/new/', views.addDiscounts, name='add_discounts'),
    path('discounts/edit/<int:discount_id>/', views.addDiscounts, name='edit_discounts'),
    path('markups/new/', views.addRaise, name='add_raise'),
    path('markups/edit/<int:raise_id>/', views.addRaise, name='edit_raise'),

    ############## EXTRAS ###################
    path('extra-costs/', views.extraCosts, name='extra_costs'),
    path('extra-costs/new/', views.editExtraCosts, name='add_extra_costs'),
    path('extra-costs/<int:extra_id>/edit/', views.editExtraCosts, name='edit_extra_costs'),
    path('get_extra_details/<int:extra_id>/', get_extra_details_view, name='get_extra_details'),
    ############## SETTINGS ###################
    path('settings/', views.Settings, name='settings'),
    # AJAX URLs for handling tariff operations
    path('save_tariff/', save_tariff, name='save_tariff'),
    path('delete_tariff/<int:tariff_id>/', delete_tariff, name='delete_tariff'),
    path('list_tariffs/', list_tariffs, name='list_tariffs'),
    path('upload/', views.file_upload, name='upload'),

















]