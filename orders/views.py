from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from orders.forms import LoginForm, CreateContactForm
from django.contrib.auth import login as log_in, authenticate
from orders.models import Contact
from django.core.exceptions import ValidationError
from django.http import HttpResponse

def login(request):
    """Вход на сайт, нужно быть зарегистрированным"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                log_in(request, user)
                return redirect('/user/product_info')
            else:
                return redirect('/user/404')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            log_in(request, user)
            return redirect('/user/registration/contact')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def get_username(request):
    """Получение id пользователя"""
    if request.user.is_authenticated:
        user_id = request.user.id
        return user_id

def registration_contact(request):
    """Регистрация контакта"""
    user_id = get_username(request)

    if request.method == 'POST':

        form = CreateContactForm(request.POST)

        if form.is_valid():
            organization = form.cleaned_data.get('organization')
            city = form.cleaned_data.get('city')
            street = form.cleaned_data.get('street')
            house = form.cleaned_data.get('house')
            structure = form.cleaned_data.get('structure')
            building = form.cleaned_data.get('building')
            apartment = form.cleaned_data.get('apartment')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            provider = form.cleaned_data.get('provider')

            contact = Contact.objects.create(user_id=user_id,
                                             organization=organization,
                                             city=city,
                                             street=street,
                                             house=house,
                                             structure=structure,
                                             building=building,
                                             apartment=apartment,
                                             phone=phone,
                                             email=email,
                                             provider=provider)
            contact.save()
            print(contact.id)



            #user = authenticate(username=username, password=password)
            # if user is not None:
            #     log_in(request, user)
            #     return redirect('/user/product_info')
            # else:
            #     return redirect('/user/registration')
    else:
        form = CreateContactForm()

    return render(request, 'signup_contact.html', {'form': form})


def four_hundred_four(request):
    '''Ошибка 404'''
    return render(request, '404.html')


def product_info(request):
    return render(request, 'product.html', {'form': 'form'})