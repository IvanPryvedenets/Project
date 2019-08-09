from django import forms
from .models import *


# Форма коментаря
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'user_email', 'message']

    user_name = forms.CharField(max_length=50, required=True)
    user_email = forms.EmailField(max_length=50, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=200)

    user_name.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваше ім'я"})
    user_email.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваш Email"})
    message.widget.attrs.update({'class': 'form-control', 'rows': 4})


# Форма замовлення
class OrderForm(forms.ModelForm):

    PAY_WAY = (
        ('Приват24', 'Приват24'),
        ('Оплата при отриманні', 'Оплата при отриманні')
    )

    TRANSPORTER = (
        ('Нова пошта', 'Нова пошта'),
        ('Укрпошта', 'Укрпошта')
    )

    AREA = (
        ('Вінницька', 'Вінницька'),
        ('Волинська', 'Волинська'),
        ('Дніпропетровська', 'Дніпропетровська'),
        ('Донецька', 'Донецька'),
        ('Житомирська', 'Житомирська'),
        ('Закарпатська', 'Закарпатська'),
        ('Запорізька', 'Запорізька'),
        ('Івано-Франківська', 'Івано-Франківська'),
        ('Київська', 'Київська'),
        ('Кіровоградська', 'Кіровоградська'),
        ('Луганська', 'Луганська'),
        ('Львівська', 'Львівська'),
        ('Миколаївська', 'Миколаївська'),
        ('Одеська', 'Одеська'),
        ('Полтавська', 'Полтавська'),
        ('Рівненська', 'Рівненська'),
        ('Сумська', 'Сумська'),
        ('Тернопільська', 'Тернопільська'),
        ('Харківська', 'Харківська'),
        ('Херсонська', 'Херсонська'),
        ('Хмельницька', 'Хмельницька'),
        ('Черкаська', 'Черкаська'),
        ('Чернівецька', 'Чернівецька'),
        ('Чернігівська', 'Чернігівська'),
    )

    class Meta:
        model = Order
        fields = ['buyer_name', 'buyer_lastname', 'buyer_email', 'buyer_tel', 'pay_way', 'transporter', 'area', 'city', 'department', 'wish']

    buyer_name = forms.CharField(max_length=15, required=True)
    buyer_lastname = forms.CharField(max_length=25, required=True)
    buyer_tel = forms.CharField(max_length=17, required=True)
    buyer_email = forms.EmailField(max_length=30, required=True)
    pay_way = forms.ChoiceField(choices=PAY_WAY)
    transporter = forms.ChoiceField(choices=TRANSPORTER)
    area = forms.ChoiceField(choices=AREA)
    city = forms.CharField(max_length=20)
    department = forms.CharField(max_length=40)
    wish = forms.CharField(widget=forms.Textarea, required=False)

    buyer_name.widget.attrs.update({'class': 'form-control'})
    buyer_lastname.widget.attrs.update({'class': 'form-control'})
    buyer_tel.widget.attrs.update({'class': 'form-control', 'data-mask': '+38(000)000-00-00'})
    buyer_email.widget.attrs.update({'class': 'form-control'})
    pay_way.widget.attrs.update({'class': 'form-control'})
    transporter.widget.attrs.update({'class': 'form-control'})
    area.widget.attrs.update({'class': 'form-control'})
    city.widget.attrs.update({'class': 'form-control'})
    department.widget.attrs.update({'class': 'form-control'})
    wish.widget.attrs.update({'class': 'form-control', 'rows': 4})


class PasswordForm(forms.Form):

    fields = ['password_1', 'password_2']

    password_1 = forms.CharField(label='Введіть пароль', widget=forms.PasswordInput, required=True, max_length=20, min_length=7)
    password_2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput, required=True, max_length=20, min_length=7)

    password_1.widget.attrs.update({'class': 'form-control', 'name': 'password_1'})
    password_2.widget.attrs.update({'class': 'form-control', 'name': 'password_2'})


class ChangeSettings(forms.Form):

    fields = ['name', 'last_name', 'login', 'email']

    name = forms.CharField(label="Ваше ім'я", max_length=15)
    last_name = forms.CharField(label='Ваше прізвище', max_length=25)
    login = forms.CharField(label='Ваш телефон', max_length=17, min_length=17)
    email = forms.EmailField(label='Ваш Email', max_length=30)

    name.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваше ім'я"})
    last_name.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваше прізвище"})
    login.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваш телефон", 'data-mask': '+38(000)000-00-00'})
    email.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваше Email"})


class UserLoginForm(forms.Form):

    fields = ['username', 'password']

    username = forms.CharField(label='Телефон', max_length=17, min_length=17)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваш телефон", 'data-mask': '+38(000)000-00-00'})
    password.widget.attrs.update({'class': 'form-control', 'placeholder': "Ваш пароль"})


class EmailForm(forms.Form):

    fields = ['email']

    email = forms.EmailField(label='Ваш Email', max_length=30)

    email.widget.attrs.update({'class': 'form-control'})


class ChangePasswordForm(forms.Form):

    fields = ['password_1', 'password_2']

    password_1 = forms.CharField(widget=forms.PasswordInput, label='Введіть пароль', required=True, max_length=20, min_length=7)
    password_2 = forms.CharField(widget=forms.PasswordInput, label='Підтвердьте пароль', required=True, max_length=20, min_length=7)

    password_1.widget.attrs.update({'class': 'form-control'})
    password_2.widget.attrs.update({'class': 'form-control'})
