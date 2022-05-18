from rest_framework import serializers
from .models import Level, Subject, Attendance, User

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'subjectId', 'count']
        
class UserSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'level', 'attendance']      

    def get_attendance(self, obj):
            att_query = Attendance.objects.filter(
                studentId=obj.id
            )
            if self.context:
                if self.context["subjectId"]:
                    att_query = Attendance.objects.filter(
                    studentId=obj.id, subjectId=self.context['subjectId'])
                
            serializer = AttendanceSerializer(att_query, many=True)
    
            return serializer.data
