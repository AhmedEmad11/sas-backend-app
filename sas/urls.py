from django.contrib import admin
from django.urls import path

from .views import (
    getSubjectAttendance,
    markAttendance,
    getProfile,
    getSubject,
    logout,
    getLevels,
    getLevelSubjects,
    overview,
    getLevelStudents
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", overview, name="overview"),  
    path('login', obtain_auth_token, name='login'),
    path('logout', logout, name='logout'),
    path('getSubjectAttendance/<int:subject>/', getSubjectAttendance, name="getSubjectAttendance"),
    path('markAttendance/', markAttendance, name="markAttendance"),
    path('getProfile', getProfile, name='getProfile'),
    path('getSubject', getSubject, name='getSubject'),
    path('getLevels', getLevels, name='getLevels'),
    path('getLevelSubjects/<int:level>/', getLevelSubjects, name='getLevelSubjects'),
    path('getLevelStudents/<int:level>/', getLevelStudents, name='getLevelStudents')
]
