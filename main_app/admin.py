from django.contrib import admin
from .models import *
# Register your models here.
from leaflet.admin import LeafletGeoAdmin  # Import LeafletGeoAdmin

admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(CarExtras)
admin.site.register(VehicleRegistrationCertificate)
admin.site.register(Extras)
admin.site.register(CarGallery)
admin.site.register(Season)
admin.site.register(Rate)
admin.site.register(CarDetails)
admin.site.register(CarFeatures)
admin.site.register(CarAudioFeatures)
admin.site.register(Mileage)
admin.site.register(Insurance)
admin.site.register(Company)
admin.site.register(WorkingHours)
admin.site.register(Discount)
admin.site.register(Raise)
admin.site.register(Tariff)
admin.site.register(Booking)
admin.site.register(BookingService)
admin.site.register(Payment)
admin.site.register(LocationType)
admin.site.register(Delivery)
admin.site.register(Country)

@admin.register(City)
class CityAdmin(LeafletGeoAdmin):  # Use LeafletGeoAdmin instead of OSMGeoAdmin
    list_display = ('name', 'location')
    search_fields = ('name', )