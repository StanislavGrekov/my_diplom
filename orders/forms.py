from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as log_in, authenticate
from orders.models import Contact


class LoginForm(forms.Form):
    """Форма для входа в сервис"""
    username = forms.CharField(max_length=30, help_text="Введите логин")
    password = forms.CharField(max_length=30, help_text="Введите пароль")

class SignUpForm(UserCreationForm):
    """Форма для регистрации"""
    first_name = forms.CharField(max_length=30, required=True, help_text='Введите фамилию', label='Фамилия')
    last_name = forms.CharField(max_length=30, required=True, help_text='Введите имя', label='Имя')
    email = forms.EmailField  (max_length=30, required=True, help_text='Введите имя', label='Эл.адрес')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateContactForm(forms.Form):
    """Форма для регистрации контакта"""
    organization = forms.CharField(max_length=100, label='Организация', help_text="Введите название организации")
    city = forms.CharField(max_length=50, label='Город',  help_text='Введите название город')
    street = forms.CharField(max_length=100, label='Улица', help_text='Введите название улицы')
    house = forms.CharField(max_length=15, label='Дом', help_text='Введите номер дома')
    structure = forms.CharField(max_length=15, label='Корпус', help_text='Введите корпус')
    apartment = forms.CharField(max_length=15, label='Номер квартиры',  help_text='Введите номер квартиры')
    phone = forms.CharField(max_length=20, label='Номер телефона', help_text='Введите телеонный номер для связи')
    provider = forms.BooleanField(label='Поставщик', help_text='Если Вы являетесь поставщиком, отметьте это поле', required=False)


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
                return render(request, '404.html')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password)

            User.objects.filter(username=username).update(first_name=first_name, last_name=last_name, email=email)
            log_in(request, user)
            return redirect('/user/registration/contact')
    else:
        form = SignUpForm()
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
            apartment = form.cleaned_data.get('apartment')
            phone = form.cleaned_data.get('phone')
            provider = form.cleaned_data.get('provider')

            contact = Contact.objects.create(user_id=user_id, organization=organization,  city=city, street=street,
                                             house=house,  structure=structure, apartment=apartment,  phone=phone,  provider=provider)

            contact.save()
            user_info = User.objects.filter(id=user_id)

            return render(request, 'signup_contact_success.html', {'user_info': user_info})
    else:
        form = CreateContactForm()

    return render(request, 'signup_contact.html', {'form': form})

