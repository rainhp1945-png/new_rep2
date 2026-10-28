from django.shortcuts import render
from .models import Owner, Reception,Service, Animal
# Create your views here.
def index(request):
    owner = Owner.objects.all()
    reception = Reception.objects.all()
    services = Service.objects.all()
    animals = Animal.objects.all()
    context = {
        'owner': owner,
        'reception': reception,
        'services': services,
        'animals': animals,
    }
    return render(request, 'index.html', context)