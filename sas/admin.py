from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Level, Attendance, Subject



class UserAdmin(UserAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'role', 'level', 'date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('id','username')
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
         (None, {
            'fields': ('id', 'username', 'role', 'level', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)

admin.site.register(Level)
admin.site.register(Subject)
admin.site.register(Attendance)