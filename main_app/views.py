from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.views import SignupView
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
    return render(request, 'index.html')
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
        if not brand or not model or not car_gallery_files or not mileage_unlimited:
            return JsonResponse({'error': 'Brand and Model are required fields. Please fill them out.'}, status=400)

        try:
            # Save data to the Car model
            car = Car.objects.create(
                brand=brand,
                model=model,
                license_plate=license_plate,
                year_of_manufacture=year_of_manufacture,
                body_color=body_color,
                body_type=body_type
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
            # You can add more logic or return success messages as needed
            return JsonResponse({'success': 'Car added successfully!'})

        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'add_car.html')
def Agents(request):
    return render(request, 'all_agents.html')

def addAgents(request):
    return render(request, 'add_agents.html')

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
def extraCosts(request):
    car_extras = CarExtras.objects.all()
    return render(request, 'all_extras.html', {'car_extras': car_extras})

def newExtraCosts(request):
    return render(request, 'add_extras.html')

def editExtraCosts(request, extra_id=None):
    extra_instance = None

    if extra_id:
        extra_instance = get_object_or_404(Extras, pk=extra_id)

    if request.method == 'POST':
        extras_form = ExtrasForm(request.POST, instance=extra_instance)
        car_extras_form = CarExtrasForm(request.POST,
                                        instance=extra_instance.car_extras if extra_instance and extra_instance.car_extras else None)

        if extras_form.is_valid() and car_extras_form.is_valid():
            extras_instance = extras_form.save()

            # If extra_instance exists, update the existing CarExtras instance
            if extra_instance and extra_instance.car_extras:
                car_extras_instance = car_extras_form.save()
            else:
                # If extra_instance doesn't exist or it doesn't have a CarExtras, create a new one
                car_extras_instance = car_extras_form.save(commit=False)
                car_extras_instance.name = extras_instance
                car_extras_instance.save()

            return redirect('extra_costs')  # Redirect to your extras list view
    else:
        extras_form = ExtrasForm(instance=extra_instance)
        car_extras_instance = extra_instance.car_extras if extra_instance and extra_instance.car_extras else None
        car_extras_form = CarExtrasForm(instance=car_extras_instance)

    return render(request, 'add_or_update_extra.html',
                  {'extras_form': extras_form, 'car_extras_form': car_extras_form})
    # return render(request, 'edit_extras.html', {'extra': extra})

############## SETTINGS ###################
def Settings(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        working_hours_formset = WorkingHoursFormSet(request.POST, prefix='working_hours', instance=Company())
        service_hours_formset = ServiceHoursFormSet(request.POST, prefix='service_hours', instance=Company())

        if form.is_valid() and working_hours_formset.is_valid() and service_hours_formset.is_valid():
            company = form.save()
            working_hours_formset.instance = company
            working_hours_formset.save()

            service_hours_formset.instance = company
            service_hours_formset.save()

            return redirect('success_page')  # Redirect to a success page
    else:
        form = CompanyForm()
        working_hours_formset = WorkingHoursFormSet(prefix='working_hours', instance=Company())
        service_hours_formset = ServiceHoursFormSet(prefix='service_hours', instance=Company())

    return render(request, 'setting.html', {'form': form, 'working_hours_formset': working_hours_formset, 'service_hours_formset': service_hours_formset})







def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        CarGallery.objects.create(image=my_file)
        return HttpResponse('')
    return JsonResponse({'post':'fasle'})