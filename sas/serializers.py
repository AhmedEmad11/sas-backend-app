from rest_framework import serializers
from .models import Level, Subject, Attendance, Role

from django.contrib.auth.models import User

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'studentId', 'subjectId', 'count', 'username', 'firstname', 'lastname']
    username = serializers.CharField(source='studentId.username')
    firstname = serializers.CharField(source='studentId.first_name')
    lastname = serializers.CharField(source='studentId.last_name')
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'username', 'firstname', 'lastname', 'role', 'level']
    username= serializers.CharField(source="user.username")
    firstname= serializers.CharField(source="user.first_name")
    lastname= serializers.CharField(source="user.last_name")
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']
    role = serializers.CharField(source='role.role')
    