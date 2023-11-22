from django.urls import path

from . import views
from .views import *
urlpatterns = [

    path('register/', RentalCompanyRegistrationView.as_view(), name='rental_company_signup'),

    ############## CARS ###################
    path('', views.home, name='home'),
    path('cars/new/', views.addCars, name='add_cars'),

    ############## USERS ###################

    ############## AGENTS ###################
    path('agents/', views.Agents, name='agents'),
    path('agents/new/', views.addAgents, name='agents_new'),

    ############## INVOICES ###################


    ############## CUSTOMERS ###################
    path('clients/', views.Customers, name='clients'),
    # path('clients/new/', views.addCustomers, name='clients_new'),

    ############## DELIVERY ###################
    path('delivery/', views.Delivery, name='delivery'),

    ############## DISCOUNTS AND PRICE RAISES ###################
    path('discounts/', views.Discounts, name='discounts'),
    path('discounts/new/', views.addDiscounts, name='add_discounts'),
    # path('discounts/edit/', views.editDiscounts, name='edit_discounts'),
    path('markups/new/', views.addRaise, name='add_raise'),
    # path('markups/edit/', views.editRaise, name='edit_raise'),

    ############## EXTRAS ###################
    path('extra-costs/', views.extraCosts, name='extra_costs'),
    path('extra-costs/new/', views.editExtraCosts, name='add_extra_costs'),
    path('extra-costs/<int:extra_id>/edit/', views.editExtraCosts, name='edit_extra_costs'),

    ############## SETTINGS ###################
    path('settings/', views.Settings, name='settings'),
    path('upload/', views.file_upload, name='upload'),

















]