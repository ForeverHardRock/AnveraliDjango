from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('performers/', views.show_performers, name='show_performers'),
    path('performers/<slug:performer_username>', views.show_performer, name='show_performer'),
    path('orders/', views.show_orders, name='show_orders'),
    path('orders/<slug:order_slug>', views.show_order, name='show_order'),
    path('new_order/', views.new_order, name='new_order'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)