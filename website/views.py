import json
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from djstripe.models import PaymentIntent
import django_filters
import stripe
from rest_framework import viewsets, filters
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from website.bank_of_georgia_api import  make_tbcbank_api_request
from main_app.models import *
from .tasks import *

def dash(request):
    return render(request, 'home.html')

def filter(request):
    return render(request, 'car_details.html')

def showCars(request):
    cities = City.objects.all()
    cars = Car.objects.all()
    context = {'cars':cars, 'cities': cities}
    return render(request, 'filter.html', context)


stripe.api_key = "sk_test_51OL3NULW8TXmjJXuTD4QizPe7nHXyvvGun6zV3FnPHM8RsCtZ378hfarx1lHyCUwsdeS71IaAyUpm6bts8kfYZu700sSal4MEU"

@csrf_exempt
def create_payment_intent(request):
    data = json.loads(request.body)
    amount_in_dollars = Decimal(data['amount'])
    print("Amount: ", amount_in_dollars)
    amount_in_cents = int(amount_in_dollars * 100)

    customer_name = data.get('customer_name', '')  # Assuming you have a 'name' field in your form
    customer_email = data.get('customer_email', '')  # Assuming you have an 'email' field in your form
    print("customer_email: ", customer_email)
    # Create or retrieve a Stripe Customer

    customer = stripe.Customer.create(
        name=customer_name,
        email=customer_email
    )
    print("customer: ", customer)
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,  # Adjust amount as needed
            currency="usd",
            customer=customer.id,
            metadata={"integration_check": "accept_a_payment"},
        )
        return JsonResponse({"clientSecret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def payment_success(request):
    # Handle success callback from TBC Bank (customize as needed)
    return render(request, 'payment_success_template.html')
def payment_error(request):
    # Handle error callback from TBC Bank (customize as needed)
    return render(request, 'payment_error_template.html')



def showCars(request):
    return render(request, 'filter.html')

# def car_list(request):
#     start_date = request.GET.get('start_date')
#     city_id = request.GET.get('city_id')
#     print(start_date)
#     end_date = request.GET.get('end_date')
#     print(end_date)
#     if city_id:
#         print(city_id)
#         cars = Car.objects.filter(city=city_id)
#     else:
#         cars = Car.objects.all()
#
#     placeholder_image_url = "URL_TO_YOUR_PLACEHOLDER_IMAGE"
#
#     car_list = []
#
#     for car in cars:
#         # Get the first image for each car
#         first_image = CarGallery.objects.filter(car=car).first()
#         image_url = first_image.image.url if first_image else None
#         car_details = CarDetails.objects.filter(car=car).first()
#         car_data = {
#             'id': car.id,
#             'brand': car.brand,
#             'model': car.model,
#             'year_of_manufacture': car.year_of_manufacture,
#             'thumbnail_url': image_url,
#             'car_details': {
#                 'engine_type': car_details.engine_type if car_details else None,
#                 'fuel_type': car_details.fuel_type if car_details else None,
#                 'transmission': car_details.transmission if car_details else None,
#                 # Add more fields as needed
#             },
#             'total_price': calculate_total_price(car, start_date, end_date),
#         }
#         # print(calculate_total_price(car, start_date, end_date))
#
#         car_list.append(car_data)
#
#     return JsonResponse({'cars': car_list})

def get_available_cars(request):
    car_id = request.GET.get('car_id')
    city_id = request.GET.get('city_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    available_cars = Car.objects.filter(city=city_id, available=True)

    # Filter out cars booked for the selected dates
    booked_cars = Booking.objects.filter(
        car__city=city_id,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).values_list('car', flat=True)

    available_cars = available_cars.exclude(id__in=booked_cars)
    print("available_cars",available_cars)

    car_list = []

    for car in available_cars:
        # Get the first image for each car
        first_image = CarGallery.objects.filter(car=car).first()
        image_url = first_image.image.url if first_image else None

        # Fetch additional details from CarDetails model
        car_details = CarDetails.objects.filter(car=car).first()


        car_city = City.objects.filter(car=car).first()

        # Call calculate_total_price function and handle None
        total_price, rate_price = calculate_total_price(car, start_date, end_date)
        if total_price is None:
            total_price = Decimal('0.00')
        if rate_price is None:
            rate_price = Decimal('0.00')

        car_data = {
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'year_of_manufacture': car.year_of_manufacture,
            'thumbnail_url': image_url,
            'car_details': {
                'engine_type': car_details.engine_type if car_details else None,
                'fuel_type': car_details.fuel_type if car_details else None,
                'transmission': car_details.transmission if car_details else None,
                # Add more fields as needed
            },
            'city': car_city.name if car_city else None,
            'total_price': total_price.quantize(Decimal('0.00'), rounding=ROUND_DOWN),
            'daily_price': rate_price.quantize(Decimal('0.00'), rounding=ROUND_DOWN),
        }

        car_list.append(car_data)
    return JsonResponse({'cars': car_list})

def calculate_total_price(car, start_date_str, end_date_str):
    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    duration = (end_date - start_date).days  # Add 1 day to include the end date
    print("Duration", duration)
    # Find applicable tariffs for the given duration
    tariffs = Tariff.objects.filter(car=car, min_days__lte=duration, max_days__gte=duration)
    print(tariffs)
    # Check if there's a matching rate for each tariff and the current season
    for tariff in tariffs:
        season = Season.objects.filter(
            start_month__lte=start_date.month,
            start_day__lte=start_date.day,
            end_month__gte=end_date.month,
            end_day__gte=end_date.day
        ).first()

        if season:
            # Check if there is a Rate that matches the current tariff, car, and season
            rate = Rate.objects.filter(
                car=car,
                tariff=tariff,
                season=season
            ).first()
            print("rate", rate)
            if rate:
                total_price = rate.price * duration  # Assuming daily rate
                print(total_price, rate.price)
                return total_price, rate.price

    return None, None  # Return None if no valid rate is found

# Assuming you have obtained start_date and end_date from the request's GET parameters
# start_date = request.GET.get('start_date')
# end_date = request.GET.get('end_date')

def car_details(request):
    car_id = request.GET.get('car_id')
    print(car_id)
    city_name = request.GET.get('city_id')  # Assuming you pass the city name in the request
    # start_date = "2023-12-18"
    # end_date = "2023-12-25"

    # Retrieve booking details from POST data
    # car_id = request.POST.get('car_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(start_date)
    print(end_date)


    try:
        car = Car.objects.get(id=car_id)
        car_details = CarDetails.objects.get(car=car)
        car_gallery = CarGallery.objects.filter(car=car)
        car_extras = CarExtras.objects.filter(cars=car)
        car_features = CarFeatures.objects.get(car=car)
        car_audio_features = CarAudioFeatures.objects.get(car=car)

        # Fetch delivery information for the specified city
        delivery_info = Delivery.objects.filter(
            Q(city__id=city_name) | Q(city=None) # Assuming location_type is related to car_details
        )

        delivery_data = []
        for delivery in delivery_info:
            delivery_data.append({
                'city': delivery.city.name if delivery.city else None,
                'location_type': delivery.location_type.name,
                'price': str(delivery.price),
                'free_from': str(delivery.free_from),
                'delivery_time': delivery.delivery_time,
            })
        print(delivery_data)
        # Fetching extra details
        extra_details = []
        for car_extra in car_extras:
            extra_details.append({
                'extra_name': car_extra.name.name,
                'price_per_day': car_extra.price_per_day,
                'minimal_price': car_extra.minimal_price,
                'maximum_price': car_extra.maximum_price,
            })

        total_price, rate_price = calculate_total_price(car, start_date, end_date)

        # Retrieve commission percentage from Django settings (you can also use a configuration file)
        commission_percentage = getattr(settings, 'COMMISSION_PERCENTAGE', 0.15)# Calculate commission
        # Calculate commission
        # Ensure both commission_percentage and total_price are Decimal
        commission_percentage = Decimal(str(commission_percentage))
        total_price = Decimal(str(total_price))
        # Calculate commission
        commission = (commission_percentage * total_price).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        # Deduct commission from total_price
        total_price_after_commission = (total_price - commission).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        car_data = {
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'year_of_manufacture': car.year_of_manufacture,
            'car_details': {
                'engine_type': car_details.engine_type,
                'capacity': car_details.capacity,
                'tank_size': car_details.tank_size,
                'fuel_consumption': car_details.fuel_consumption,
                'fuel_type': car_details.fuel_type,
                'drive_type': car_details.drive_type,
                'abs_system': car_details.abs_system,
                'ebd_system': car_details.ebd_system,
                'esp_system': car_details.esp_system,
                'transmission': car_details.transmission,
                # Add more fields as needed
            },
            'car_gallery': [
                {
                    'image_url': image.image.url,
                    # Add more fields as needed
                }
                for image in car_gallery
            ],
            'car_extras': extra_details,
            'car_features': {
                'required_license_category': car_features.required_license_category,
                'seats': car_features.seats,
                'number_of_doors': car_features.number_of_doors,
                'air_conditioning': car_features.air_conditioning,
                'interior': car_features.interior,
                'roof': car_features.roof,
                'powered_windows': car_features.powered_windows,
                'airbags': car_features.airbags,
                'side_wheel': car_features.side_wheel,
                'cruise_control': car_features.cruise_control,
                'rear_view_camera': car_features.rear_view_camera,
                'parking_assist': car_features.parking_assist,
                # Add more fields as needed
            },
            'car_audio_features': {
                'has_radio': car_audio_features.has_radio,
                'has_audio_cd': car_audio_features.has_audio_cd,
                'has_mp3': car_audio_features.has_mp3,
                'has_usb': car_audio_features.has_usb,
                'has_aux': car_audio_features.has_aux,
                'has_bluetooth': car_audio_features.has_bluetooth,
                # Add more fields as needed
            },
            'delivery_info': delivery_data if delivery_data else None,
            'total_price': total_price.quantize(Decimal('0.00'), rounding=ROUND_DOWN),
            'rate_price': rate_price.quantize(Decimal('0.00'), rounding=ROUND_DOWN),
            'commission': commission,
            'total_price_after_commission': total_price_after_commission,
        }

        return JsonResponse({'car_details': car_data})
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)
    except CarDetails.DoesNotExist:
        return JsonResponse({'error': 'Car details not found'}, status=404)
    except CarGallery.DoesNotExist:
        return JsonResponse({'error': 'Car gallery not found'}, status=404)
    except CarExtras.DoesNotExist:
        return JsonResponse({'error': 'Car extras not found'}, status=404)
    except CarFeatures.DoesNotExist:
        return JsonResponse({'error': 'Car features not found'}, status=404)
    except CarAudioFeatures.DoesNotExist:
        return JsonResponse({'error': 'Car audio features not found'}, status=404)


@csrf_exempt
def cars_near_city(request):
    if request.method == 'POST':
        city_latitude = float(request.POST.get('city_latitude'))
        city_longitude = float(request.POST.get('city_longitude'))

        # Create a Point object for the selected city
        selected_city_location = Point(city_longitude, city_latitude, srid=4326)
        print(selected_city_location)
        # Query cars near the selected city's location
        cars_near_city = Car.objects.annotate(
            distance=Distance('city__location', selected_city_location)
        ).filter()  # Adjust the distance value as needed
        print(cars_near_city)

        # Serialize the cars data as JSON
        cars_data = [{'model': car.model, 'brand': car.brand, 'location': [car.city.latitude, car.city.longitude]} for car in cars_near_city]

        return JsonResponse({'cars': cars_data})
    else:
        # Handle other HTTP methods or return an error
        return JsonResponse({'error': 'Invalid request method'})

def car_available(car_id, start_date, end_date):
    return Car.objects.filter(
        Q(id=car_id, available=True) &
        ~Q(reservation__start_date__lte=end_date, reservation__end_date__gte=start_date)
    ).exists()
def book_car(request):
    if request.method == 'POST':
        # Retrieve booking details from POST data
        car_id = request.POST.get('car_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        pickup_location = request.POST.get('pickup_location')
        pickup_time = request.POST.get('pickup_time')
        drop_location = request.POST.get('drop_location')
        drop_time = request.POST.get('drop_time')

        # Create a Booking object and save it to the database
        # (You need to import your models and handle this according to your model structure)
        # booking = Booking(car_id=car_id, start_date=start_date, end_date=end_date, ...)
        # booking.save()
        current_time = timezone.now()

        # Assuming a reservation lasts for 30 minutes
        end_time = current_time + timezone.timedelta(minutes=30)

        if car_available(car_id, start_datetime, end_datetime):
            reservation = Booking.objects.create(
                user=request.user,
                car_id=car_id,
                start_date=start_datetime,
                end_date=end_datetime
            )

        # Schedule a task to free up the car after 30 minutes
        release_reservation_after_timeout.apply_async(
            (reservation.id,),
            eta=end_time
        )


        # Dummy response for illustration purposes
        response_data = {'status': 'success', 'message': 'Booking successful!'}

        return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@transaction.atomic
def create_booking(request):
    # city_id = 1
    # car_id = 1
    # start_date = "2023-12-18"
    # end_date = "2023-12-25"

    # Retrieve booking details from POST data
    city_id = request.POST.get('city_id')
    car_id = request.POST.get('car_id')
    start_date = request.POST.get('start_date')
    print(start_date)
    end_date = request.POST.get('end_date')
    print(start_date)
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    pickup_location = request.POST.get('pickup_location')
    pickup_time = request.POST.get('pickup_time')
    drop_location = request.POST.get('drop_location')
    drop_time = request.POST.get('drop_time')
    customer_name = request.POST.get('customer_name')
    customer_email = request.POST.get('customer_email')

    # Retrieve car and convert date strings to datetime objects
    car = get_object_or_404(Car, id=car_id)
    start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Calculate the duration of the booking
    duration = (end_date - start_date).days  # Add 1 day to include the end date
    print(duration)
    # Find applicable tariffs for the given duration
    tariffs = Tariff.objects.filter(car=car, min_days__lte=duration, max_days__gte=duration)
    print(tariffs)
    # Check if there's a matching rate for each tariff and the current season
    total_price = None
    for tariff in tariffs:
        season = Season.objects.filter(
            start_month__lte=start_date.month,
            start_day__lte=start_date.day,
            end_month__gte=end_date.month,
            end_day__gte=end_date.day
        ).first()

        if season:
            # Check if there is a Rate that matches the current tariff, car, and season
            rate = Rate.objects.filter(
                car=car,
                tariff=tariff,
                season=season  # Use the Season object directly here
            ).first()

        if rate:
            total_price = rate.price * duration  # Assuming daily rate
            print(total_price)
            break  # Exit the loop if a valid rate is found

    if total_price is not None:
        # Perform validation on customer data


        customer, created = Customer.objects.get_or_create(
            email="alimoeed15@g.com",
            defaults={
                'name': "moeed",
                # ... Set other customer-related fields with default values
            }
        )
        # For testing purposes, set some pickup and drop times
        pickup_time = timezone.datetime.strptime('12:00:00', '%H:%M:%S').time()
        drop_time = timezone.datetime.strptime('14:00:00', '%H:%M:%S').time()
        pickup_location = "Airport"
        drop_location = "Rental Office"

        # Fetch delivery prices for the selected locations
        pickup_delivery_price = get_delivery_price(pickup_location, city_id)
        print("pickup_delivery_price", pickup_delivery_price)
        drop_delivery_price = get_delivery_price(drop_location, city_id)
        print("drop_delivery_price", drop_delivery_price)
        # Add delivery prices to the total_price
        if pickup_delivery_price is not None:
            total_price += pickup_delivery_price
            print("After pickup_delivery_price", total_price)

        if drop_delivery_price is not None:
            total_price += drop_delivery_price
            print("After drop_delivery_price", total_price)

        # Check for existing bookings for the same car and overlapping dates
        existing_bookings = Booking.objects.filter(
            car=car,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        print(existing_bookings)

        if existing_bookings.exists():
            return HttpResponse('Error: A booking for this car and overlapping dates already exists.')

        # Create the booking
        booking = Booking.objects.create(customer=customer, car=car, start_date=start_date, end_date=end_date,
                pickup_time=pickup_time,pickup_location = pickup_location, drop_location = drop_location,
                drop_time=drop_time)

        # Schedule the Celery task to release the reservation after a timeout
        # release_reservation_after_timeout.apply_async(args=[booking.id], countdown=120)  # 1 hour timeout
        # print()
        # Handle selected services
        selected_services = request.POST.getlist('selected_services')

        # For testing purposes, let's assume you have some services in your database
        test_service_ids = [1]  # Replace with actual service IDs from your database

        service = CarExtras.objects.get(id=1)
        quantity = 2  # Set a quantity for testing purposes
        # Calculate service price based on quantity and price_per_day
        service_price = service.price_per_day * int(quantity)
        print(service, service_price)
        # Create BookingService instance
        BookingService.objects.create(
            booking=booking,
            car_extra=service,
            quantity=quantity,
            service_price=service_price
        )
        # Add the service price to the total booking price
        total_price += service_price
        print("After Services", total_price)

        # Create the payment associated with the booking
        payment = Payment.objects.create(booking=booking, amount=total_price)
        car.available = False
        car.save()
        # Handle payment logic here (redirect to payment gateway, etc.)

        return HttpResponse(f'Booking created. Total price: {total_price}')
    else:
        # Handle the case where no matching tariff is found
        return HttpResponse('Error: No matching tariff found for the given duration and season.')


def get_delivery_price(location_name, city_id):
    # Assuming 'location_name' is a string representing the location name
    # 'city_id' is the ID of the city associated with the delivery
    delivery = Delivery.objects.filter(city_id=city_id, location_type__name=location_name).first()
    print("Delivery", delivery)
    return delivery.price if delivery else None


def privacy_policy(request):
    return render(request, 'privacy_policy.html')