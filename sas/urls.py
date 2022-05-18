from django.urls import path

from .views import (
    getSubjectAttendance,
    markAttendance,
    getProfile,
    getSubjects,
    logout,
    getLevels,
    getLevelSubjects,
    overview,
    getLevelStudents,
    createAttendanceForLevel
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", overview, name="overview"),  
    path('login', obtain_auth_token, name='login'),
    path('logout', logout, name='logout'),
    path('getSubjectAttendance/<int:level>/<int:subject>/', getSubjectAttendance, name="getSubjectAttendance"),
    path('markAttendance/', markAttendance, name="markAttendance"),
    path('getProfile', getProfile, name='getProfile'),
    path('getSubjects', getSubjects, name='getSubject'),
    path('getLevels', getLevels, name='getLevels'),
    path('getLevelSubjects/<int:level>/', getLevelSubjects, name='getLevelSubjects'),
    path('getLevelStudents/<int:level>/', getLevelStudents, name='getLevelStudents'),
    path('createAttendanceForLevel/', createAttendanceForLevel, name='createAttendanceForLevel')
]
