from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request, pk):
    pk = pk
    return render(request, 'index.html', {'pk': pk})