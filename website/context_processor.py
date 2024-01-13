from main_app.models import City


def cities(request):
    city = City.objects.all()
    context = {'city' : city}
    return context