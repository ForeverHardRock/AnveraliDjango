import random

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


class Orders(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликовано'),
        ('in_work', 'В работе'),
        ('done', 'Выполнено'),
    )
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID заказа')
    title = models.CharField(max_length=100, verbose_name='Название заказа')
    slug = models.CharField(max_length=255, verbose_name='URL заказа', null=True, blank=True, unique=True)
    description = models.TextField(verbose_name='Описание заказа')
    price = models.FloatField(verbose_name='Стоимость')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published', verbose_name='Статус заказа')
    customer = models.CharField(max_length=10, verbose_name='ID заказчика')
    performer = models.CharField(max_length=10, verbose_name='ID исполнителя', null=True, blank=True)
    potential_performers = models.JSONField(verbose_name='IDs потенциальных исполнителей', default=list)
    customer_done = models.BooleanField(verbose_name='Подтверждение готовности от заказчика', default=False)
    performer_done = models.BooleanField(verbose_name='Подтверждение готовности от исполнителя', default=False)
    date = models.DateTimeField(verbose_name='Дата публикации', default=timezone.now())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title)) + str(random.randint(0, 9999999))
        super(Orders, self).save(*args, **kwargs)


