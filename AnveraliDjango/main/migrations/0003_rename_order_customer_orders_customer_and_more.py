# Generated by Django 5.0.4 on 2024-04-22 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_orders_order_customer_alter_orders_order_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='order_customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_performer',
            new_name='performer',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_slug',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_title',
            new_name='title',
        ),
    ]
