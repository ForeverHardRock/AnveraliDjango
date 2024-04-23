from django.shortcuts import render, redirect, get_object_or_404

from .forms import OrderForm
from .models import Orders
from django.core.paginator import Paginator
from django.apps import apps


def home(request):
    user = request.user
    home_data = None
    home_link = None
    home_link_text = None
    acc_type = None
    home_ul = None
    if user.is_authenticated:
        acc_type = user.acc_type
        if user.acc_type == 'performer':
            home_data = Orders.objects.filter(status='published').order_by('-date')[:5]
            home_link = 'show_orders'
            home_ul = 'Свежайшие заказы:'
            home_link_text = 'Посмотреть все заказы'
        elif user.acc_type == 'customer':
            AllUsers = apps.get_model('accounts', 'AllUsers')
            home_data = AllUsers.objects.filter(acc_type='performer').order_by('-last_login')[:5]
            home_link = 'show_performers'
            home_ul = 'Активные исполнители:'
            home_link_text = 'Посмотреть всех исполнителей'

    context = {
        'home_data': home_data,
        'home_link': home_link,
        'home_ul': home_ul,
        'home_link_text': home_link_text,
        'acc_type': acc_type,
    }
    return render(request, 'main/home.html', context=context)


def show_performers(request):
    user = request.user

    if user.is_authenticated:
        AllUsers = apps.get_model('accounts', 'AllUsers')
        performers_list = AllUsers.objects.filter(acc_type='performer').order_by('-last_login')
        paginator = Paginator(performers_list, 10)
        page_number = request.GET.get('page')
        performers = paginator.get_page(page_number)

        context = {
            'performers': performers,
        }

        return render(request, 'main/performers.html', context=context)
    return redirect('home')


def show_performer(request, performer_username: str):
    user = request.user

    if user.is_authenticated:
        AllUsers = apps.get_model('accounts', 'AllUsers')
        performer_user = AllUsers.objects.get(username=performer_username)

        context = {
            'performer_user': performer_user,
        }

        return render(request, 'main/performer.html', context=context)
    return redirect('home')


def show_orders(request):
    user = request.user

    if user.is_authenticated:
        all_orders = Orders.objects.filter(status='published').order_by('-date')
        paginator = Paginator(all_orders, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        context = {
            'orders': orders,
        }

        return render(request, 'main/orders.html', context=context)
    return redirect('home')


def show_order(request, order_slug: str):
    user = request.user

    if user.is_authenticated:
        order = get_object_or_404(Orders, slug=order_slug)
        if order.status == 'published' or str(order.customer) == str(user.id) or str(order.performer) == str(user.id):
            performers_list = None
            if request.method == 'POST' and 'Показать отклики' not in request.POST:
                if 'Откликнуться' in request.POST:
                    order.potential_performers.append(user.id)
                    order.save()

                elif 'Работа выполнена' in request.POST:
                    if user.acc_type == 'performer':
                        order.performer_done = True
                    elif user.acc_type == 'customer':
                        order.customer_done = True
                    if order.customer_done and order.performer_done:
                        order.status = 'done'
                        AllUsers = apps.get_model('accounts', 'AllUsers')
                        customer_user = AllUsers.objects.get(id=order.customer)
                        customer_user.spending += order.price
                        customer_user.save()
                    order.save()

                elif 'perf_accept' in request.POST:
                    order.status = 'in_work'
                    order.performer = request.POST.get('perf_accept')
                    order.save()

            elif request.method == 'POST' and 'Показать отклики' in request.POST:
                AllUsers = apps.get_model('accounts', 'AllUsers')
                performers_list = AllUsers.objects.filter(id__in=order.potential_performers)

            # Надпись, что работа выполнена
            if order.status == 'done':
                dynamic_field = 'Работа выполнена'
                type_field = 'str'

            # Кнопка откликнуться за исполнителя
            elif user.acc_type == 'performer' and order.status == 'published' and user.id not in order.potential_performers:
                dynamic_field = 'Откликнуться'
                type_field = 'btn'

            # Надпись что уже откликался за исполнителя
            elif user.acc_type == 'performer' and order.status == 'published' and user.id in order.potential_performers:
                dynamic_field = 'Заявка на выполнение подана'
                type_field = 'str'

            # Кнопка "готово" за исполнителя
            elif str(order.performer) == str(user.id) and order.status == 'in_work' and order.performer_done is False:
                dynamic_field = 'Работа выполнена'
                type_field = 'btn'

            # Надпись что нажато "готово" за исполнителя
            elif str(order.performer) == str(user.id) and order.status == 'in_work' and order.performer_done is True:
                dynamic_field = 'Заявка о выполнении работы подана. Ожидайте ответа заказчика.'
                type_field = 'str'

            # Надпись, что откликов нет за заказчика
            elif str(order.customer) == str(user.id) and order.status == 'published' and len(order.potential_performers) == 0:
                dynamic_field = 'Пока что никто не откликнулся на ваше задание'
                type_field = 'str'

            # Кнопка показать откликнувшихся за заказчика
            elif str(order.customer) == str(user.id) and order.status == 'published' and len(order.potential_performers) > 0:
                dynamic_field = 'Показать отклики'
                type_field = 'btn'

            # Кнопка "готово" за заказчика
            elif str(order.customer) == str(user.id) and order.status == 'in_work' and order.customer_done is False:
                dynamic_field = 'Работа выполнена'
                type_field = 'btn'

            # Надпись что нажато "готово" за исполнителя
            elif str(order.customer) == str(user.id) and order.status == 'in_work'and order.customer_done is True:
                dynamic_field = 'Заявка о выполнении работы подана. Ожидайте ответа исполнителя.'
                type_field = 'str'

            else:
                dynamic_field = None
                type_field = None

            context = {
                'order': order,
                'dynamic_field': dynamic_field,
                'type_field': type_field,
                'performers_list': performers_list,
            }
            return render(request, 'main/order.html', context=context)

    return redirect('home')


def new_order(request):
    user = request.user
    if user.acc_type == 'customer':
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.customer = user.id
                order.save()
                return redirect('cabinet')

        form = OrderForm()
        return render(request, 'main/new_order.html', {'form': form})
    return redirect('home')
