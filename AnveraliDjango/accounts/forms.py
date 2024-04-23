from django import forms
from .models import AllUsers
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['email', 'username', 'first_name', 'last_name', 'photo', 'number', 'spending', 'rating', 'is_active', 'last_login', 'date_joined']
        labels = {
            'email': 'Email',
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
            'spending': 'Потриченные средства',
            'rating': 'Рейтинг',
            'is_active': 'Подтвержденный аккаунт',
            'last_login': 'Дата последнего входа',
            'date_joined': 'Дата регистрации',
        }


class CustomerRegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='Подтверждение пароль', widget=forms.PasswordInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = AllUsers
        fields = ['email', 'username', 'password', 'password_confirmation', 'first_name', 'last_name', 'photo', 'number']
        labels = {
            'email': 'Email',
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('customer_password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise ValidationError("Пароли не совпадают. Пожалуйста, введите пароли еще раз.")

        return cleaned_data


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['first_name', 'last_name', 'photo', 'number']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
        }


class PerformerRegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='Подтверждение пароль', widget=forms.PasswordInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = AllUsers
        fields = ['email', 'username', 'password', 'password_confirmation', 'first_name', 'last_name', 'photo', 'number', 'exp']
        labels = {
            'email': 'Email',
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
            'exp': 'Опыт работы',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Пароли не совпадают. Пожалуйста, введите пароли еще раз.")
        return cleaned_data


class PerformerEditForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['first_name', 'last_name', 'photo', 'number', 'exp']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
            'exp': 'Опыт работы',
        }


class PerformerAdminForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['email', 'username', 'first_name', 'last_name', 'photo', 'number', 'exp', 'rating', 'is_active', 'last_login', 'date_joined']
        labels = {
            'email': 'Email ',
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'number': 'Номер телефона',
            'exp': 'Опыт',
            'rating': 'Рейтинг',
            'is_active': 'Подтвержденный аккаунт',
            'last_login': 'Дата последнего входа',
            'date_joined': 'Дата регистрации',
        }


class AdminAdminForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['email', 'username', 'first_name', 'last_name', 'photo', 'number', 'is_superuser', 'is_staff', 'user_permissions', 'last_login']


