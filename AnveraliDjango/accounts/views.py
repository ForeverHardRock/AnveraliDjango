from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.http import Http404

from .models import AllUsers
from django.contrib.auth.tokens import default_token_generator
from .forms import LoginForm, PerformerRegistrationForm, CustomerRegistrationForm, PerformerEditForm, CustomerEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .backends import NewBackend
from django.apps import apps


def edit_profile(request):
    user = request.user
    if user:
        if request.method == 'POST':
            if user.acc_type == 'performer':
                form = PerformerEditForm(request.POST, request.FILES)
            elif user.acc_type == 'customer':
                form = CustomerEditForm(request.POST, request.FILES)
            else:
                form = None
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                if form.cleaned_data['photo']:
                    user.photo = form.cleaned_data['photo']
                user.number = form.cleaned_data['number']
                user.exp = form.cleaned_data['exp']
                user.save()
                return redirect('cabinet')

        if user.acc_type == 'performer':
            form = PerformerEditForm(request.POST or None, request.FILES or None, instance=user)
        elif user.acc_type == 'customer':
            form = CustomerEditForm(request.POST or None, request.FILES or None, instance=user)
        else:
            form = None
        context = {
            'form': form,
            'form_type': 'Редактирование профиля'
        }
        return render(request, 'accounts/signup.html', context=context)
    return redirect('home')


def cabinet(request):
    Orders = apps.get_model('main', 'Orders')
    user = request.user
    if user:
        user_orders = None
        job_title = None
        new_order = False
        if user.acc_type == 'customer':
            user_orders = Orders.objects.filter(customer=user.id)
            job_title = 'Ваши опубликованные работы:'
            new_order = True
        elif user.acc_type == 'performer':
            user_orders = Orders.objects.filter(performer=user.id)
            job_title = 'Ваши принятые работы:'

        context = {
            'user_orders': user_orders,
            'job_title': job_title,
            'new_order': new_order,
        }
        return render(request, 'accounts/cabinet.html', context=context)
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = NewBackend().authenticate(request,
                                             username=username,
                                             password=password,)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'login_error': 'Неверное имя пользователя или пароль'})

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def pre_signup(request):
    return render(request, 'accounts/pre_signup.html')


def signup(request, acc_type: str):

    if acc_type == 'performer':
        form = PerformerRegistrationForm(request.POST, request.FILES)
    elif acc_type == 'customer':
        form = CustomerRegistrationForm(request.POST, request.FILES)
    else:
        raise Http404("Страница не найдена")

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.acc_type = acc_type
            user.password = make_password(password=user.password)
            user.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = account_activation_token.make_token(user)
            mail_subject = 'Подтверждение регистрации на сайте "Anverali Freelance"'
            message = render_to_string('accounts/acc_active_mail.html', {
                'user': user.first_name,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })

            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()
            return render(request, 'accounts/status_page.html', {'stat': 'На Ваш E-Mail отправлено письмо для '
                                                                        'подтверждения регистации'})

    else:
        if acc_type == 'performer':
            form = PerformerRegistrationForm()
        elif acc_type == 'customer':
            form = CustomerRegistrationForm()
        else:
            form = None
    context = {
        'form': form,
        'form_type': 'Регистрация'
    }
    return render(request, 'accounts/signup.html', context=context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AllUsers.objects.get(id=uid)

    except Exception as ex:
        print(ex)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/status_page.html',
                      {'stat': 'Благодарим за регистрацию на сайте! Теперь Вы можете войти!'})
    else:
        return render(request, 'accounts/status_page.html',
                      {'stat': 'Ссылка недействительна'})


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = AllUsers.objects.get(email=email)
                user_name = user.username
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
                subject = 'Сброс пароля на сайте "Anverali Freelance"'
                message = render_to_string('password/reset_email.html', {
                    'user': user_name,
                    'reset_url': reset_url,
                })

                send_email = EmailMessage(
                    subject, message, to=[email]
                )
                send_email.send()
                return render(request, 'password/reset_done.html')
            except Exception as err:
                print(err)
                cont = {
                    'form': form,
                    'check_mail': 'Пользователь с таким email не найден, попробуйте еще раз.'
                        }
                return render(request, 'password/reset_form.html', context=cont)
    else:
        form = PasswordResetForm()
    cont = {
        'form': form,
        'check_mail': 'Введите E-Mail от Вашего аккаунта, на него будет отправлено письмо с ссылкой по сбросу пароля.'
    }
    return render(request, 'password/reset_form.html', context=cont)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/reset_complete.html'

