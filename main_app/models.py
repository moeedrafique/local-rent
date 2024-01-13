from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(default=None, null=True, blank=True)
    longitude = models.FloatField(default=None, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"


# Create your models here.
class Company(models.Model):
    name_of_company = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    legal_name_of_business = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)  # Adjust the max_length based on your requirements
    second_phone = models.CharField(max_length=15, blank=True, null=True)  # Adjust the max_length based on your requirements
    country = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    central_office_location = models.ForeignKey(City, on_delete=models.CASCADE, default=None, null=True, blank=True)
    email = models.EmailField()
    web_site = models.URLField()
    central_office_address = models.TextField()

    def __str__(self):
        return f"{self.name_of_company} - Language: {self.language} - Legal Name: {self.legal_name_of_business} - Phone: {self.phone} - Country: {self.country}"


class CustomUser(AbstractUser):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True)
    country = models.CharField(max_length=100)


class Car(models.Model):
    dealer = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None, null=True, blank=True)
    brand = models.CharField(max_length=255, default=None)
    model = models.CharField(max_length=255, default=None)
    license_plate = models.CharField(max_length=20, unique=True, default=None)
    year_of_manufacture = models.CharField(max_length=50, blank=True, null=True)
    body_color = models.CharField(max_length=50, default=None)
    body_type = models.CharField(max_length=50, default=None)
    available = models.BooleanField(default=True)
    PENDING_MODERATION = 'Pending Moderation'
    AVAILABLE_FOR_SALE = 'Available for Sale'
    INTERNAL_USE_ONLY = 'Internal Use Only'

    STATUS_CHOICES = [
        (PENDING_MODERATION, 'Pending Moderation'),
        (AVAILABLE_FOR_SALE, 'Available for Sale'),
        (INTERNAL_USE_ONLY, 'Internal Use Only'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING_MODERATION)
    moderation_date = models.DateField(null=True, blank=True)

    def save_for_sale(self):
        self.status = self.AVAILABLE_FOR_SALE
        self.save()

    def save_for_internal_use(self):
        self.status = self.INTERNAL_USE_ONLY
        self.save()

    def __str__(self):
        return f"Car: {self.brand}{self.model} , Status: {self.status}"

class Extras(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CarExtras(models.Model):
    name = models.ForeignKey(Extras, on_delete=models.CASCADE, related_name='car_extras')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    minimal_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    maximum_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    cars = models.ManyToManyField('Car', related_name='extras', blank=True)

    def __str__(self):
        return self.name.name

class CarGallery(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='car_gallery/')

    def __str__(self):
        return f"{self.car} - {self.image}"

class Season(models.Model):
    name = models.CharField(max_length=255)
    start_month = models.IntegerField()  # Assuming 1-12 for January-December
    start_day = models.IntegerField()
    end_month = models.IntegerField()
    end_day = models.IntegerField()

class Tariff(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    min_days = models.IntegerField()
    max_days = models.IntegerField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car} - {self.min_days} to {self.max_days} days"

class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Mileage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    unlimited_mileage = models.BooleanField(default=False)
    limited_mileage = models.PositiveIntegerField(null=True, blank=True)
    overage_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f" Unlimited: {self.unlimited_mileage} - Limited: {self.limited_mileage} - Overage Fee: {self.overage_fee}"

class Insurance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    # insurance_company = models.CharField(max_length=255)
    # policy_number = models.CharField(max_length=30, unique=True)
    # coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # start_date = models.DateField()
    # end_date = models.DateField()
    franchise = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.car}"


class CarDetails(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    engine_type = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=5, decimal_places=2)
    tank_size = models.DecimalField(max_digits=6, decimal_places=2)
    fuel_consumption = models.DecimalField(max_digits=4, decimal_places=2)

    fuel_type = models.CharField(max_length=50)
    drive_type = models.CharField(max_length=50)
    abs_system = models.BooleanField(default=False)
    ebd_system = models.BooleanField(default=False)
    esp_system = models.BooleanField(default=False)
    transmission = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.engine_type} - {self.capacity}L - Tank: {self.tank_size}L - Consumption: {self.fuel_consumption}l/100km - {self.fuel_type} - {self.drive_type} - ABS: {self.abs_system}, EBD: {self.ebd_system}, ESP: {self.esp_system} - Transmission: {self.transmission}"

class CarFeatures(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    required_license_category = models.CharField(max_length=50, blank=True, null=True)
    seats = models.CharField(max_length=50, blank=True, null=True)
    number_of_doors = models.CharField(max_length=50, blank=True, null=True)
    air_conditioning = models.CharField(max_length=50, blank=True, null=True)
    interior = models.CharField(max_length=50, blank=True, null=True)
    roof = models.CharField(max_length=50, blank=True, null=True)
    powered_windows = models.CharField(max_length=50, blank=True, null=True)
    airbags = models.CharField(max_length=50, blank=True, null=True)
    side_wheel = models.CharField(max_length=50, blank=True, null=True)
    cruise_control = models.BooleanField(default=False)
    rear_view_camera = models.BooleanField(default=False)
    parking_assist = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Required License: {self.required_license_category} - Seats: {self.seats} - "
            f"Doors: {self.number_of_doors} - AC: {self.air_conditioning} - "
            f"Interior: {self.interior} - Roof: {self.roof} - Powered Windows: {self.powered_windows} - "
            f"Airbags: {self.airbags} - Side Wheel: {self.side_wheel} - "
            f"Cruise Control: {self.cruise_control} - Rear View Camera: {self.rear_view_camera} - "
            f"Parking Assist: {self.parking_assist}"
        )

class CarAudioFeatures(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    has_radio = models.BooleanField(default=False)
    has_audio_cd = models.BooleanField(default=False)
    has_mp3 = models.BooleanField(default=False)
    has_usb = models.BooleanField(default=False)
    has_aux = models.BooleanField(default=False)
    has_bluetooth = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Radio: {self.has_radio} - Audio CD: {self.has_audio_cd} - "
            f"MP3: {self.has_mp3} - USB: {self.has_usb} - AUX: {self.has_aux} - "
            f"Bluetooth: {self.has_bluetooth}"
        )



class VehicleRegistrationCertificate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='vehicle_registration_certificate/', default=None)
    # registration_number = models.CharField(max_length=20, unique=True)
    # registration_date = models.DateField(blank=True, null=True)
    # owner_name = models.CharField(max_length=255)
    # owner_address = models.TextField()
    # engine_number = models.CharField(max_length=30, unique=True)
    # chassis_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.car} - {self.image}"

#
#
#
#
#
#
# class Agent(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)  # Adjust the max_length based on your requirements
#     percent = models.DecimalField(max_digits=5,
#                                   decimal_places=2)  # Adjust the max_digits and decimal_places based on your requirements
#
#     def __str__(self):
#         return f"{self.name} - Email: {self.email} - Phone: {self.phone} - Percent: {self.percent}%"



class WorkingHours(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    preparation_time = models.DurationField(default='00:30')

    def __str__(self):
        return f"{self.company.name_of_company} - {self.day_of_week} - {self.opening_time} to {self.closing_time}"

class ServiceAtNonBusinessHours(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    additional_charge = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company.name_of_company} - Additional Charge: {self.additional_charge}"


class Discount(models.Model):
    name = models.CharField(max_length=255)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    cars = models.ManyToManyField('Car', related_name='discounts', blank=True)

    def __str__(self):
        return self.name


class Raise(models.Model):
    name = models.CharField(max_length=255)
    valid_from = models.DateField()
    valid_to = models.DateField()
    raise_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    cars = models.ManyToManyField('Car', related_name='raise_cars', blank=True)

    def __str__(self):
        return self.name

class LocationType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None, null=True, blank=True)
    location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    free_from = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField()  # Assuming delivery time is in minutes

    def __str__(self):
        return f"{self.city} ({self.location_type})"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    primary_phone = models.CharField(max_length=15, blank=True, null=True)
    is_primary_whatsapp = models.BooleanField(default=False, blank=True, null=True)
    is_primary_viber = models.BooleanField(default=False, blank=True, null=True)
    is_primary_telegram = models.BooleanField(default=False, blank=True, null=True)
    secondary_phone = models.CharField(max_length=15, blank=True, null=True)
    is_secondary_whatsapp = models.BooleanField(default=False, blank=True, null=True)
    is_secondary_viber = models.BooleanField(default=False, blank=True, null=True)
    is_secondary_telegram = models.BooleanField(default=False, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class BookingService(models.Model):
    booking = models.ForeignKey('Booking', related_name='selected_services', on_delete=models.CASCADE)
    car_extra = models.ForeignKey(CarExtras, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    pickup_location = models.CharField(max_length=255)
    pickup_time = models.TimeField(blank=True, null=True)
    drop_location = models.CharField(max_length=255)
    drop_time = models.TimeField(blank=True, null=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be equal to or after the start date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.car} from {self.start_date} to {self.end_date} "

list_of_reservation_ids = Booking.objects.values_list('id', flat=True)

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"
    
# by {self.user.username}