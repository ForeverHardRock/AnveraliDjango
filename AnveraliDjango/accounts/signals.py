from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.utils import timezone

from .models import AllUsers

my_groups = {
    'admin': 'Администраторы',
    'performer': 'Исполнители',
    'customer': 'Заказчики',
}


@receiver(post_save, sender=AllUsers)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.acc_type:
            group_name = instance.acc_type
            group = Group.objects.get(name=my_groups[group_name])
            instance.groups.add(group)


@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    user.last_login = timezone.now()
    user.save()
