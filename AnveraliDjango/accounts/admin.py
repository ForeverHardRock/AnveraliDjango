from django.contrib import admin
from .models import AllUsers
from .forms import PerformerAdminForm, CustomerAdminForm, AdminAdminForm
from django.utils.html import format_html


@admin.register(AllUsers)
class AllUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'acc_type', 'username', 'rating', 'image_preview']
    ordering = ['id']
    search_field = ['name']
    list_per_page = 20

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.acc_type == 'performer':
            self.form = PerformerAdminForm
        elif obj and obj.acc_type == 'customer':
            self.form = CustomerAdminForm
        elif obj and obj.acc_type == 'admin':
            self.form = AdminAdminForm
        else:
            self.form = super().get_form(request, obj, **kwargs)
        return self.form

    def image_preview(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" style="max-width: 100px; max-height: 100px;">')
        else:
            return 'No image'

    image_preview.short_description = 'Фото'


