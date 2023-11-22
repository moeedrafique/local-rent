from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django.forms import inlineformset_factory

from .models import *

# rental_app/forms.py

from allauth.account.forms import SignupForm
from django_countries.widgets import CountrySelectWidget

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

WorkingHoursFormSet = inlineformset_factory(Company, WorkingHours, fields='__all__')
ServiceHoursFormSet = inlineformset_factory(Company, ServiceAtNonBusinessHours, fields='__all__')

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'license_plate', 'year_of_manufacture', 'body_color', 'body_type']

CarGalleryFormSet = inlineformset_factory(Car, CarGallery, fields=['image'], extra=1)
PriceAndConditionsFormSet = inlineformset_factory(Car, PriceAndConditions, fields=['service_name', 'price', 'conditions'], extra=1)
MileageFormSet = inlineformset_factory(Car, Mileage, fields=['unlimited_mileage', 'limited_mileage', 'overage_fee'], extra=1)
InsuranceFormSet = inlineformset_factory(Car, Insurance, fields=['franchise', 'deposit'], extra=1)
CarDetailsFormSet = inlineformset_factory(Car, CarDetails, fields=['engine_type', 'capacity', 'tank_size', 'fuel_consumption', 'fuel_type', 'drive_type', 'abs_system', 'ebd_system', 'esp_system', 'transmission'], extra=1)
CarFeaturesFormSet = inlineformset_factory(Car, CarFeatures, fields=['required_license_category', 'seats', 'number_of_doors', 'air_conditioning', 'interior', 'roof', 'powered_windows', 'airbags', 'side_wheel', 'cruise_control', 'rear_view_camera', 'parking_assist'], extra=1)
CarAudioFeaturesFormSet = inlineformset_factory(Car, CarAudioFeatures, fields=['has_radio', 'has_audio_cd', 'has_mp3', 'has_usb', 'has_aux', 'has_bluetooth'], extra=1)
# VehicleRegistrationCertificateFormSet = inlineformset_factory(Car, VehicleRegistrationCertificate, fields=['registration_number', 'owner_name', 'owner_address', 'engine_number', 'chassis_number'], extra=1)

class RentalCompanyRegistrationView(SignupForm):
    company_name = forms.CharField(max_length=100, label='Company Name')
    country = CountryField(blank_label='Select Country',).formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'})
    )
    # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super(RentalCompanyRegistrationView, self).__init__(*args, **kwargs)
        # Exclude the 'username' field
        if 'username' in self.fields:
            del self.fields['username']


    def save(self, request):
        user = super(RentalCompanyRegistrationView, self).save(request)
        user.company_name = self.cleaned_data['company_name']
        user.country = self.cleaned_data['country']
        user.save()
        return user

class ExtrasForm(forms.ModelForm):
    # Override the default widget for the 'name' field to use a select box
    name = forms.ModelChoiceField(queryset=Extras.objects.all(), to_field_name='name', empty_label=None)
    class Meta:
        model = Extras
        fields = ['name']

class CarExtrasForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(queryset=Car.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = CarExtras
        exclude = ['name']

class DiscountForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(queryset=Car.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Discount
        fields = ['name', 'valid_from', 'valid_to', 'discount_percentage', 'cars']

    # Override the default widget for the 'valid_from' and 'valid_to' fields to use date input
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class RaiseForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(queryset=Car.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Raise
        fields = ['name', 'valid_from', 'valid_to', 'raise_percentage', 'cars']

    # Override the default widget for the 'valid_from' and 'valid_to' fields to use date input
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
# class RentalCompanyRegistrationForm(SignupForm):
#     company_name = forms.CharField(max_length=100, label='Company Name')
#     country = CountryField().formfield()
#     email = forms.EmailField()
#     password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
#
#     def __init__(self, *args, **kwargs):
#         super(RentalCompanyRegistrationForm, self).__init__(*args, **kwargs)
#         # Exclude the 'username' field
#         if 'username' in self.fields:
#             del self.fields['username']
#
#     def save(self, request):
#         user = super(RentalCompanyRegistrationForm, self).save(request)
#         user.company_name = self.cleaned_data.get('company_name')
#         user.country = self.cleaned_data.get('country')
#         user.email = self.cleaned_data.get('email')
#         user.set_password(self.cleaned_data.get('password1'))
#         user.save()
#         return user
