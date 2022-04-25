from django.contrib import admin
from .models import Role, Level, Subject, Attendance

admin.site.register(Role)
admin.site.register(Level)
admin.site.register(Subject)
admin.site.register(Attendance)

