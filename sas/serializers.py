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
        fields = ['id', 'studentId', 'subjectId', 'count', 'username', 'firstname']
    username = serializers.CharField(source='studentId.username')
    firstname = serializers.CharField(source='studentId')
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstname', 'lastname', 'role', 'levelName', 'levelId']
    role = serializers.CharField(source='role.role')
    levelName = serializers.CharField(source='role.level.name')
    levelId = serializers.CharField(source='role.level.id')