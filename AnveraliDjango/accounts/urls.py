from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('signup/', views.pre_signup, name='pre_signup'),
    path('signup/<slug:acc_type>/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('reset_password/', views.password_reset, name='reset_password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
