# Generated by Django 5.0.4 on 2024-04-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_orders_potential_performers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='potential_performers',
            field=models.JSONField(default=list, verbose_name='IDs потенциальных исполнителей'),
        ),
    ]
