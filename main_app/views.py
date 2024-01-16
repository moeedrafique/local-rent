from decimal import Decimal

from django.contrib import messages
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.views import SignupView
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
# Create your views here.

############## AUTHENTICATION ###################



class RentalCompanyRegistrationView(SignupView):
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # Custom logic for processing the form, if needed
        return super(RentalCompanyRegistrationView, self).form_valid(form)

############## CARS ###################
def home(request):
    cars_with_bookings = Car.objects.filter(
        booking__isnull=False,
        dealer=request.user.company_name
    ).distinct().prefetch_related('booking_set')
    context = {'cars_with_bookings': cars_with_bookings}
    return render(request, 'index.html', context)


def all_cars(request):
    cars = Car.objects.filter(dealer=request.user.company_name)
    context = {'cars':cars}
    return render(request, 'all_cars.html', context)


def carsList(request):
    # Filter cars that have bookings and belong to the user's company
    cars_with_bookings = Car.objects.filter(
        booking__isnull=False,
        dealer=request.user.company_name
    ).distinct().prefetch_related('booking_set')
    context = {'cars_with_bookings':cars_with_bookings}
    return render(request, 'all_bookings.html', context)

def convert_to_boolean(value):
    return value == 'on'
# def addCars(request):
#     if request.method == 'POST':
#         car_form = CarForm(request.POST)
#         car_gallery_formset = CarGalleryFormSet(request.POST, request.FILES, prefix='car_gallery')
#         price_and_conditions_formset = PriceAndConditionsFormSet(request.POST, prefix='price_and_conditions')
#         mileage_formset = MileageFormSet(request.POST, prefix='mileage')
#         insurance_formset = InsuranceFormSet(request.POST, prefix='insurance')
#         car_details_formset = CarDetailsFormSet(request.POST, prefix='car_details')
#         car_features_formset = CarFeaturesFormSet(request.POST, prefix='car_features')
#         car_audio_features_formset = CarAudioFeaturesFormSet(request.POST, prefix='car_audio_features')
#         # registration_certificate_formset = VehicleRegistrationCertificateFormSet(request.POST, prefix='registration_certificate')
#
#         if (
#             car_form.is_valid() and mileage_formset.is_valid()
#                 # and car_gallery_formset.is_valid() and price_and_conditions_formset.is_valid() and
#             #  and insurance_formset.is_valid() and car_details_formset.is_valid() and
#             # car_features_formset.is_valid() and car_audio_features_formset.is_valid()
#             # registration_certificate_formset.is_valid()
#         ):
#             car = car_form.save()
#
#             # car_gallery_formset.instance = car
#             # car_gallery_formset.save()
#             #
#             # price_and_conditions_formset.instance = car
#             # price_and_conditions_formset.save()
#
#             mileage_formset.instance = car
#             mileage_formset.save()
#
#             # insurance_formset.instance = car
#             # insurance_formset.save()
#             #
#             # car_details_formset.instance = car
#             # car_details_formset.save()
#             #
#             # car_features_formset.instance = car
#             # car_features_formset.save()
#             #
#             # car_audio_features_formset.instance = car
#             # car_audio_features_formset.save()
#             #
#             # registration_certificate_formset.instance = car
#             # registration_certificate_formset.save()
#
#             print("HELLLLLLLLLL")
#
#     else:
#         car_form = CarForm()
#         car_gallery_formset = CarGalleryFormSet(prefix='car_gallery')
#         price_and_conditions_formset = PriceAndConditionsFormSet(prefix='price_and_conditions')
#         mileage_formset = MileageFormSet(prefix='mileage')
#         insurance_formset = InsuranceFormSet(prefix='insurance')
#         car_details_formset = CarDetailsFormSet(prefix='car_details')
#         car_features_formset = CarFeaturesFormSet(prefix='car_features')
#         car_audio_features_formset = CarAudioFeaturesFormSet(prefix='car_audio_features')
#         # registration_certificate_formset = VehicleRegistrationCertificateFormSet(prefix='registration_certificate')
#
#     # Render your template with the formsets
#     return render(request, 'add_car.html', {
#         'car_form': car_form,
#         'car_gallery_formset': car_gallery_formset,
#         'price_and_conditions_formset': price_and_conditions_formset,
#         'mileage_formset': mileage_formset,
#         'insurance_formset': insurance_formset,
#         'car_details_formset': car_details_formset,
#         'car_features_formset': car_features_formset,
#         'car_audio_features_formset': car_audio_features_formset,
#         # 'registration_certificate_formset': registration_certificate_formset,
#     })
############## USERS ###################


############## AGENTS ###################


def addCars(request):
    # Fetch all extras and annotate with a concatenated string of prices for each extra
    extras = Extras.objects.prefetch_related('car_extras').distinct()
    tariff = Tariff.objects.filter(dealer=request.user.company_name)
    season = Season.objects.filter()

    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        license_plate = request.POST.get('license_plate')
        year_of_manufacture = request.POST.get('year_of_manufacture')
        body_color = request.POST.get('body_color')
        body_type = request.POST.get('body_type')
        car_gallery_files = request.FILES.getlist('car_gallery')
        mileage_unlimited = convert_to_boolean(request.POST.get('mileage_unlimited'))
        mileage_limited = request.POST.get('mileage_limited')
        mileage_overage_fee = request.POST.get('mileage_overage_fee')


        engine_type = request.POST.get('engine_type')
        engine_capacity = request.POST.get('engine_capacity')
        fuel_type = request.POST.get('fuel_type')
        tank_size = request.POST.get('tank_size')
        fuel_consumption = request.POST.get('fuel_consumption')
        transmission = request.POST.get('transmission')
        drive_type = request.POST.get('drive_type')
        abs_system = convert_to_boolean(request.POST.get('abs_system'))
        ebd_system = convert_to_boolean(request.POST.get('ebd_system'))
        esp_system = convert_to_boolean(request.POST.get('esp_system'))


        required_license_category = request.POST.get('required_license_category')
        seats = request.POST.get('seats')
        number_of_doors = request.POST.get('number_of_doors')
        air_conditioning = request.POST.get('air_conditioning')
        interior = request.POST.get('interior')
        roof = request.POST.get('roof')
        powered_windows = request.POST.get('powered_windows')
        airbags = request.POST.get('airbags')
        side_wheel = request.POST.get('side_wheel')
        cruise_control = convert_to_boolean(request.POST.get('cruise_control'))
        rear_view_camera = convert_to_boolean(request.POST.get('rear_view_camera'))
        parking_assist = convert_to_boolean(request.POST.get('parking_assist'))
        print(cruise_control, rear_view_camera, parking_assist)

        has_radio = convert_to_boolean(request.POST.get('has_radio'))
        has_audio_cd = convert_to_boolean(request.POST.get('has_audio_cd'))
        has_mp3 = convert_to_boolean(request.POST.get('has_mp3'))
        has_usb = convert_to_boolean(request.POST.get('has_usb'))
        has_aux = convert_to_boolean(request.POST.get('has_aux'))
        has_bluetooth = convert_to_boolean(request.POST.get('has_bluetooth'))

        vehicle_registration_certificate = request.POST.get('vehicle_registration_certificate')

        print(mileage_unlimited)
        print("Eng", esp_system, ebd_system, abs_system)
        print("Audio", has_radio, has_audio_cd, has_mp3, has_usb, has_aux,  has_bluetooth)

        # Validate the data
        if not brand or not model:
            return JsonResponse({'error': 'Brand and Model are required fields. Please fill them out.'}, status=400)

        try:
            # company = Company.objects.filter()
            # Save data to the Car model
            car = Car.objects.create(
                brand=brand,
                model=model,
                license_plate=license_plate,
                year_of_manufacture=year_of_manufacture,
                body_color=body_color,
                body_type=body_type
            )
            car.dealer = request.user.company_name
            print(car.dealer)
            car.city = request.user.company_name.central_office_location
            print(car.city)
            car.save()

            # Update or create rates
            for key, value in request.POST.items():
                if key.startswith('rate_price_'):
                    parts = key.split('_')
                    print(len(parts))
                    if len(parts) == 4:
                        _, _, season_id, tariff_id = parts
                        price = request.POST.get(key)

                        if season_id and tariff_id and price:
                            car_id = request.POST.get(f'rate_car_{season_id}_{tariff_id}')
                            rate, created = Rate.objects.update_or_create(
                                car_id=car_id,
                                season_id=season_id,
                                tariff_id=tariff_id,
                                defaults={'price': Decimal(price)}
                            )

            # Create the Mileage object only when everything is successful
            mileage = Mileage.objects.create(car=car, unlimited_mileage=mileage_unlimited, limited_mileage=mileage_limited,
                                   overage_fee=mileage_overage_fee)
            print(mileage)

            # Handle car gallery files
            for file in car_gallery_files:
                # Do something with each file, such as save it to the server or associate it with the car model
                CarGallery.objects.create(car=car, image=file)
            #

            # Create the CarAudioFeatures object
            audio_features = CarAudioFeatures.objects.create(
                car=car,
                has_radio=has_radio,
                has_audio_cd=has_audio_cd,
                has_mp3=has_mp3,
                has_usb=has_usb,
                has_aux=has_aux,
                has_bluetooth=has_bluetooth
            )

            # Create the CarDetails object
            details = CarDetails.objects.create(
                car=car,
                engine_type=engine_type,
                capacity=engine_capacity,
                fuel_type=fuel_type,
                tank_size=tank_size,
                fuel_consumption=fuel_consumption,
                transmission=transmission,
                drive_type=drive_type,
                abs_system=abs_system,
                ebd_system=ebd_system,
                esp_system=esp_system
            )
            print(details)

            # # Create the CarFeatures object
            features = CarFeatures.objects.create(
                car=car,
                required_license_category=required_license_category,
                seats=seats,
                number_of_doors=number_of_doors,
                air_conditioning=air_conditioning,
                interior=interior,
                roof=roof,
                powered_windows=powered_windows,
                airbags=airbags,
                side_wheel=side_wheel,
            )
            registration = VehicleRegistrationCertificate.objects.create(
                car=car,
                image=vehicle_registration_certificate,
            )
            print(features)
            if car_id:
                messages.success(request, 'Car updated successfully!')
            else:
                messages.success(request, 'Car added successfully!')
            return redirect('all_cars')  # Redirect to the car list page
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': str(e)}, status=500)
    context = {
        'extras': extras,
        'season': season,
        'tariff': tariff,
    }
    return render(request, 'add_car.html', context)

def edit_car(request, car_id):
    # Fetch all extras and annotate with a concatenated string of prices for each extra
    extras = Extras.objects.prefetch_related('car_extras').distinct()
    tariff = Tariff.objects.filter(dealer=request.user.company_name)
    season = Season.objects.filter()

    car = get_object_or_404(Car, id=car_id)
    mileage, created = Mileage.objects.get_or_create(car=car)
    car_gallery = CarGallery.objects.filter(car=car)
    audio_features = CarAudioFeatures.objects.get(car=car)
    details = CarDetails.objects.get(car=car)
    features = CarFeatures.objects.get(car=car)
    existing_rates = Rate.objects.filter(car=car)
    registration = VehicleRegistrationCertificate.objects.filter(car=car)


    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        license_plate = request.POST.get('license_plate')
        year_of_manufacture = request.POST.get('year_of_manufacture')
        body_color = request.POST.get('body_color')
        body_type = request.POST.get('body_type')
        car_gallery_files = request.FILES.getlist('car_gallery')
        mileage_unlimited = convert_to_boolean(request.POST.get('mileage_unlimited'))
        mileage_limited = request.POST.get('mileage_limited')
        mileage_overage_fee = request.POST.get('mileage_overage_fee')


        engine_type = request.POST.get('engine_type')
        engine_capacity = request.POST.get('engine_capacity')
        fuel_type = request.POST.get('fuel_type')
        tank_size = request.POST.get('tank_size')
        fuel_consumption = request.POST.get('fuel_consumption')
        transmission = request.POST.get('transmission')
        drive_type = request.POST.get('drive_type')
        abs_system = convert_to_boolean(request.POST.get('abs_system'))
        ebd_system = convert_to_boolean(request.POST.get('ebd_system'))
        esp_system = convert_to_boolean(request.POST.get('esp_system'))


        required_license_category = request.POST.get('required_license_category')
        seats = request.POST.get('seats')
        number_of_doors = request.POST.get('number_of_doors')
        air_conditioning = request.POST.get('air_conditioning')
        interior = request.POST.get('interior')
        roof = request.POST.get('roof')
        powered_windows = request.POST.get('powered_windows')
        airbags = request.POST.get('airbags')
        side_wheel = request.POST.get('side_wheel')
        cruise_control = convert_to_boolean(request.POST.get('cruise_control'))
        rear_view_camera = convert_to_boolean(request.POST.get('rear_view_camera'))
        parking_assist = convert_to_boolean(request.POST.get('parking_assist'))
        print(cruise_control, rear_view_camera, parking_assist)



        has_radio = convert_to_boolean(request.POST.get('has_radio'))
        has_audio_cd = convert_to_boolean(request.POST.get('has_audio_cd'))
        has_mp3 = convert_to_boolean(request.POST.get('has_mp3'))
        has_usb = convert_to_boolean(request.POST.get('has_usb'))
        has_aux = convert_to_boolean(request.POST.get('has_aux'))
        has_bluetooth = convert_to_boolean(request.POST.get('has_bluetooth'))

        vehicle_registration_certificate = request.POST.get('vehicle_registration_certificate')

        print(mileage_unlimited)
        print("Eng", esp_system, ebd_system, abs_system)
        print("Audio", has_radio, has_audio_cd, has_mp3, has_usb, has_aux,  has_bluetooth)

        # Validate the data
        if not brand or not model:
            return JsonResponse({'error': 'Brand and Model are required fields. Please fill them out.'}, status=400)

        try:
            # company = Company.objects.filter()
            # Save data to the Car model
            # Update car details
            car.brand = brand
            car.model = model
            car.license_plate = license_plate
            car.year_of_manufacture = year_of_manufacture
            car.body_color = body_color
            car.body_type = body_type

            car.save()
            print("Check Car")

            # Update or create rates
            for key, value in request.POST.items():
                if key.startswith('rate_price_'):
                    parts = key.split('_')
                    print(len(parts))
                    if len(parts) == 4:
                        _, _, season_id, tariff_id = parts
                        price = request.POST.get(key)

                        if season_id and tariff_id and price:
                            car_id = request.POST.get(f'rate_car_{season_id}_{tariff_id}')
                            rate, created = Rate.objects.update_or_create(
                                car_id=car_id,
                                season_id=season_id,
                                tariff_id=tariff_id,
                                defaults={'price': Decimal(price)}
                            )
            # Add the following line to check the values received in the request
            print(request.POST.items())

            # Update Mileage object
            mileage.unlimited_mileage = mileage_unlimited
            mileage.limited_mileage = mileage_limited
            mileage.overage_fee = mileage_overage_fee
            mileage.save()
            print("Check mileage")
            # Handle car gallery files
            for file in car_gallery_files:
                # Do something with each file, such as save it to the server or associate it with the car model
                CarGallery.objects.create(car=car, image=file)
            #


            # Update CarAudioFeatures object
            audio_features.has_radio = has_radio
            audio_features.has_audio_cd = has_audio_cd
            audio_features.has_mp3 = has_mp3
            audio_features.has_usb = has_usb
            audio_features.has_aux = has_aux
            audio_features.has_bluetooth = has_bluetooth
            audio_features.save()
            print("Check audio_features")
            # Update CarDetails object
            details.engine_type = engine_type
            details.capacity = engine_capacity
            details.fuel_type = fuel_type
            details.tank_size = tank_size
            details.fuel_consumption = fuel_consumption
            details.transmission = transmission
            details.drive_type = drive_type
            details.abs_system = abs_system
            details.ebd_system = ebd_system
            details.esp_system = esp_system

            details.save()
            print("Check details")
            # Update CarFeatures object
            features.required_license_category = required_license_category
            features.seats = seats
            features.number_of_doors = number_of_doors
            features.air_conditioning = air_conditioning
            features.interior = interior
            features.roof = roof
            features.powered_windows = powered_windows
            features.airbags = airbags
            features.side_wheel = side_wheel
            features.cruise_control = cruise_control
            features.rear_view_camera = rear_view_camera
            features.parking_assist = parking_assist
            features.save()
            print("Check features")

            # Update VehicleRegistrationCertificate object
            registration = VehicleRegistrationCertificate.objects.create(
                car=car,
                image=vehicle_registration_certificate,
            )
            print("Check registration")

            print(features)
            if car_id:
                messages.success(request, 'Car updated successfully!')
            else:
                messages.success(request, 'Car added successfully!')
            return redirect('all_cars')  # Redirect to the car list page
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': str(e)}, status=500)

    context = {
        'extras': extras,
        'season': season,
        'tariff': tariff,
        'car': car,
        'mileage': mileage,
        'car_gallery': car_gallery,
        'audio_features': audio_features,
        'details': details,
        'features': features,
        'registration': registration,
        'existing_rates': existing_rates,
    }

    return render(request, 'edit_car.html', context)


def Agents(request):
    return render(request, 'all_agents.html')

def addAgents(request):
    return render(request, 'add_agent.html')

############## INOVOICES ###################


############## CUSTOMERS ###################
def Customers(request):
    return render(request, 'all_clients.html')

# def addCustomers(request):
#     return render(request, 'add_clients.html')

############## DELIVERY ###################
def Delivery(request):
    return render(request, 'all_delivery.html')

############## DISCOUNTS AND PRICE RAISES ###################
def Discounts(request):
    car_discount = Discount.objects.all()
    add_raise = Raise.objects.all()
    return render(request, 'all_discounts.html', {'car_discount': car_discount, 'add_raise': add_raise})

def addDiscounts(request, discount_id=None):
    cars = Car.objects.all()
    discount_instance = None

    if discount_id:
        discount_instance = get_object_or_404(Discount, pk=discount_id)

    if request.method == 'POST':
        discount_form = DiscountForm(request.POST, instance=discount_instance)

        if discount_form.is_valid():
            discount_form.save()
            return redirect('discounts')  # Redirect to your discounts list view
    else:
        discount_form = DiscountForm(instance=discount_instance)

    return render(request, 'add_discounts.html', {'discount_form': discount_form, 'cars': cars})

# def editDiscounts(request):
#     return render(request, 'edit_discounts.html')

def addRaise(request, raise_id=None):
    cars = Car.objects.all()
    raise_instance = None

    if raise_id:
        raise_instance = get_object_or_404(Raise, pk=raise_id)

    if request.method == 'POST':
        raise_form = RaiseForm(request.POST, instance=raise_instance)

        if raise_form.is_valid():
            raise_form.save()
            return redirect('discounts')  # Redirect to your discounts list view
    else:
        raise_form = RaiseForm(instance=raise_instance)

    return render(request, 'add_raise.html', {'raise_form': raise_form, 'cars': cars})

# def editRaise(request):
#     return render(request, 'edit_raise.html')

############## EXTRAS ###################
def get_extra_details_view(request, extra_id):
    try:
        # Filter instead of get, as there can be multiple CarExtras with the same name
        extras_list = CarExtras.objects.filter(id=extra_id)

        # Handle the case where there are no CarExtras
        if not extras_list.exists():
            return JsonResponse({'error': 'No CarExtras found for the given Extras ID'}, status=404)

        # Assuming you want to return details of the first CarExtras
        extra = extras_list.first()

        extra_details = {
            'price_per_day': str(extra.price_per_day),
            'minimal_price': str(extra.minimal_price),
            'maximum_price': str(extra.maximum_price),
        }

        return JsonResponse(extra_details)

    except CarExtras.DoesNotExist:
        # Handle the case where no CarExtras are found
        return JsonResponse({'error': 'CarExtras not found for the given Extras ID'}, status=404)
    except CarExtras.MultipleObjectsReturned:
        # Handle the case where multiple CarExtras are found
        return JsonResponse({'error': 'Multiple CarExtras found for the given Extras ID'}, status=500)

def extraCosts(request):
    car_extras = CarExtras.objects.all()
    return render(request, 'all_extras.html', {'car_extras': car_extras})

def newExtraCosts(request):
    return render(request, 'add_extras.html')

def editExtraCosts(request, extra_id=None):
    extra_instance = None

    if extra_id:
        extra_instance = get_object_or_404(CarExtras, pk=extra_id)

    if request.method == 'POST':
        extras_form = ExtrasForm(request.POST, instance=extra_instance)
        car_extras_form = CarExtrasForm(request.POST,
                                        instance=extra_instance if extra_instance else None)

        if extras_form.is_valid() and car_extras_form.is_valid():
            extras_instance = extras_form.save()

            # If extra_instance exists, update the existing CarExtras instance
            if extra_instance:
                car_extras_instance = car_extras_form.save()
            else:
                # If extra_instance doesn't exist or it doesn't have a CarExtras, create a new one
                car_extras_instance = car_extras_form.save(commit=False)
                car_extras_instance.name = extras_instance
                car_extras_instance.save()

            return redirect('extra_costs')  # Redirect to your extras list view
    else:
        extras_form = ExtrasForm(instance=extra_instance)
        car_extras_instance = extra_instance if extra_instance and extra_instance else None
        car_extras_form = CarExtrasForm(instance=car_extras_instance)

    return render(request, 'add_or_update_extra.html',
                  {'extras_form': extras_form, 'car_extras_form': car_extras_form})
    # return render(request, 'edit_extras.html', {'extra': extra})

############## SETTINGS ###################
def Settings(request):
    user = request.user
    tariff = Tariff.objects.filter(dealer=user.company_name)
    if request.method == 'POST':
        # If the form is submitted
        name_of_company = request.POST.get('name_of_company')
        language = request.POST.get('language')
        legal_name_of_business = request.POST.get('legal_name')
        # ... get other form fields ...
        min_days_list = request.POST.getlist('minDays[]')
        max_days_list = request.POST.getlist('maxDays[]')
        try:
            # Retrieve the existing company associated with the current user
            company = user.company_name
            company.company_name = name_of_company
            company.language = language
            company.legal_name_of_business = legal_name_of_business
            # ... set other fields ...

            company.full_clean()  # Perform model validation
            company.save()

            # Validate and save the data
            for min_days, max_days in zip(min_days_list, max_days_list):
                Tariff.objects.create(
                    dealer=company,
                    min_days=min_days,
                    max_days=max_days,
                )

            messages.success(request, 'Settings saved successfully!')
        except ValidationError as e:
            # Handle validation errors
            error_messages = e.message_dict.values()
            return render(request, 'setting.html', {'error_messages': error_messages})

    else:
        # If it's a GET request, populate the form with existing company data
        # You can use this data to pre-fill the form fields in your template
        company_data = {
            'name_of_company': user.company_name.name_of_company,
            'language': user.company_name.language,
            'legal_name_of_business': user.company_name.legal_name_of_business,
            # ... get other fields ...
        }
        return render(request, 'setting.html', {'company_data': company_data, 'tariff':tariff})

@csrf_exempt
def save_tariff(request):
    if request.method == 'POST':
        try:
            # Get data from the POST request
            min_days = request.POST.get('minDays')
            max_days = request.POST.get('maxDays')

            # Check if the tariff ID is provided for updating an existing tariff
            tariff_id = request.POST.get('tariffId')
            if tariff_id:
                # Update existing tariff
                tariff = Tariff.objects.get(pk=tariff_id)
                tariff.min_days = min_days
                tariff.max_days = max_days
                tariff.save()
            else:
                # Create a new tariff
                tariff = Tariff.objects.create(dealer=request.user.company_name, min_days=min_days, max_days=max_days)

            return JsonResponse({'status': 'success', 'tariff_id': tariff.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def delete_tariff(request, tariff_id):
    if request.method == 'DELETE':
        try:
            tariff = Tariff.objects.get(pk=tariff_id)

            # Delete tariff logic
            tariff.delete()

            return JsonResponse({'status': 'success'})
        except Tariff.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tariff not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def list_tariffs(request):
    if request.method == 'GET':
        # Retrieve tariff data
        tariffs = [{'id': tariff.id, 'min_days': tariff.min_days, 'max_days': tariff.max_days} for tariff in Tariff.objects.all()]

        return JsonResponse({'tariffs': tariffs})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        CarGallery.objects.create(image=my_file)
        return HttpResponse('')
    return JsonResponse({'post':'fasle'})


