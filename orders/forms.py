from django import forms

class LoginForm(forms.Form):

    username = forms.CharField(max_length=30, help_text="Введите логин")
    password = forms.CharField(max_length=30, help_text="Введите пароль")


class CreateContactForm(forms.Form):

    organization = forms.CharField(max_length=100, label='Организация', help_text="Введите название организации")
    city = forms.CharField(max_length=50, label='Город',  help_text='Введите название город')
    street = forms.CharField(max_length=100, label='Улица', help_text='Введите название улицы')
    house = forms.CharField(max_length=15, label='Дом', help_text='Введите номер дома')
    structure = forms.CharField(max_length=15, label='Корпус', help_text='Введите корпус')
    building = forms.CharField(max_length=15, label='Строение', help_text='Строение')
    apartment = forms.CharField(max_length=15, label='Номер квартиры',  help_text='Введите номер квартиры')
    phone = forms.CharField(max_length=20, label='Номер телефона', help_text='Введите телеонный номер для связи')
    email = forms.EmailField(max_length=100, label='Эл.почта', help_text='Введите электронный адрес')
    provider = forms.BooleanField(label='Поставщик', help_text='Если Вы являетесь поставщиком, отметьте это поле', required=False)

