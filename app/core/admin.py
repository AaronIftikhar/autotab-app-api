""" Django admin customisation"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
""" This can change the language, if we ever need to do that !"""

from core import models

class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users """
    ordering = ['id']
    list_display = ['email','name','company_name']
    fieldsets = (
        (None, {'fields':('email','password')}),
        (
            _('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields':('last_login',)}),
    )

    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                )
            }),
    )

# class ProjectAdmin(admin.ModelAdmin):
#     fields = ('name', 'phone', 'created_at')

admin.site.register(models.User,UserAdmin)
admin.site.register(models.Project)
admin.site.register(models.ProjectInstance)