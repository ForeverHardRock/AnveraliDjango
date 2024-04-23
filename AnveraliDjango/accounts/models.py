from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

ACCOUNT_TYPES = [
        ('customer', 'Заказчик'),
        ('performer', 'Исполнитель'),
        ('admin', 'Админ')
    ]
RATING_CHOICES = [(i/10, i/10) for i in range(0, 51)]
VALIDATOR = [MinValueValidator(0.0), MaxValueValidator(5.0)]


class AllUsers(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    acc_type = models.CharField(max_length=10, verbose_name='Тип аккаунта', choices=ACCOUNT_TYPES)
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(unique=True, max_length=100, verbose_name='Логин')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    photo = models.ImageField(upload_to='users_photo/', verbose_name='Фото', null=True, blank=True)
    number = models.CharField(max_length=20, verbose_name='Номер', null=True, blank=True)
    spending = models.FloatField(verbose_name='Потраченные средства', default=0)
    exp = models.TextField(verbose_name='Опыт', null=True, blank=True)
    rating = models.FloatField(
        verbose_name='Рейтинг',
        validators=VALIDATOR,
        choices=RATING_CHOICES,
        default=0
    )
    is_active = models.BooleanField(default=False, verbose_name='Подтвержденный аккаунт')
    last_login = models.DateTimeField(verbose_name='Последний вход', default=timezone.now())
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now())
    REQUIRED_FIELDS = ['email', 'password', 'acc_type']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.acc_type == 'admin' and self.id is None:
            self.is_active = True
        super(AllUsers, self).save(*args, **kwargs)


