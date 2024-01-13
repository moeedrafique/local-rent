# from django.test import TestCase, Client
# from django.urls import reverse
# from django.utils import timezone
# from .models import Car, Season, Tariff, Rate, Booking
# from datetime import timedelta
#
# class BookingViewTest(TestCase):
#     def setUp(self):
#         # Create test data (cars, seasons, tariffs, rates, etc.)
#         self.car = Car.objects.create(brand='Test Car')
#         self.season = Season.objects.create(name='Test Season', start_date=timezone.now(), end_date=timezone.now() + timedelta(days=30))
#         self.tariff = Tariff.objects.create(car=self.car, min_days=1, max_days=3)
#         self.rate = Rate.objects.create(car=self.car, tariff=self.tariff, season=self.season, price=50)
#
#     def test_create_booking(self):
#         client = Client()
#
#         # Example: Test booking creation with a valid scenario
#         response = client.get(reverse('create_booking', args=(self.car.id, '2023-01-01', '2023-01-05')))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Booking created. Total price: 250', response.content.decode())
#
#         # Example: Test booking creation with an invalid scenario (no matching tariff)
#         response = client.get(reverse('create_booking', args=(self.car.id, '2023-01-01', '2023-01-10')))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Error: No matching tariff found for the given duration and season.', response.content.decode())