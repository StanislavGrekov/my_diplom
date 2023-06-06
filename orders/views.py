from django.shortcuts import render, redirect

from django.contrib.auth import login as log_in, authenticate
from orders.models import Contact
from django.core.exceptions import ValidationError
from django.http import HttpResponse


def product_info(request):
    return render(request, 'product.html', {'form': 'form'})