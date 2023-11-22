from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(CarExtras)
admin.site.register(VehicleRegistrationCertificate)
admin.site.register(Extras)
admin.site.register(CarGallery)
admin.site.register(PriceAndConditions)
admin.site.register(CarDetails)
admin.site.register(CarFeatures)
admin.site.register(CarAudioFeatures)
admin.site.register(Mileage)
admin.site.register(Insurance)
admin.site.register(Company)
admin.site.register(WorkingHours)
admin.site.register(Discount)
admin.site.register(Raise)