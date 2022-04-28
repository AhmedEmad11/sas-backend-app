from .serializers import (
    AttendanceSerializer, LevelSerializer, RoleSerializer, SubjectSerializer
)

from .models import (
    Attendance,
    Level,
    Role, 
    Subject
)

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view, 
    authentication_classes, 
    permission_classes
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 


@api_view(['GET'])
def overview(request):
    res = {
        "Route": "Description",
        "POST login": "send username & password for login",
        "POST AUTHED logout": "logout",
        "GET AUTHED getSubjectAttendance/<int:subject>/": "get the attendance for a single subject",
        "POST AUTHED markAttendance/": "send subjectId & studentId to mark attendance",
        "GET AUTHED getProfile": "get the current user profile",
        "GET AUTHED getSubject": "get the current user subjects",
        "GET AUTHED getLevels": "get the current user levels if the user is doctor or admin",
        "GET AUTHED getLevelSubjects/<int:level>/": "get the subjects of a single level"
    }
    return Response(res)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLevelStudents(request, level):
    role = request.user.role.role
    if role == 'doctor' or role == 'admin':
        students = Role.objects.filter(level=level)
        serializer = RoleSerializer(students, many=True)
        return Response(serializer.data)
    else:
        return Response("students can't use this route")
        


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubjectAttendance(request, subject):
    id = request.user.id
    role = request.user.role.role
    if role == 'doctor':
        ids = []
        subjects = Subject.objects.filter(doctor=id)
        for i in range(len(subjects)):
            ids.append(subjects[i].id)
        if subject in ids:
            queryset = Attendance.objects.filter(subjectId=subject)
            serializer = AttendanceSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("this doctor does not teach this subject")
    elif role == 'student':
        sub = get_object_or_404(Subject, id=subject)
        if sub.level == request.user.role.level:
            queryset = Attendance.objects.filter(subjectId=subject, studentId=id)
            serializer = AttendanceSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("this student does not take this subject")
    else:
        queryset = Attendance.objects.filter(subjectId=subject)
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def markAttendance(request):
    studentId = request.data["studentId"]
    subjectId = request.data["subjectId"]
    student = get_object_or_404(User, id=studentId)
    role = student.role.role
    if role == 'student':
        sub = get_object_or_404(Subject, id=subjectId)
        if sub.level == student.role.level:
            attendance, created = Attendance.objects.get_or_create(subjectId=sub, studentId=student)
            attendance.count += 1
            attendance.save()            
            return Response("success")
        else:
            return Response("this student does not take this subject")
    else:
        return Response("this user is not a student")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    res = {
        "id": user.id,
        "username": user.username,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "role": user.role.role,
        "levelName": "none",
        "levelId": "none"
    }
    if user.role.level != None:
        res["levelName"] = user.role.level.name
        res["levelId"] = user.role.level.id
    return Response(res)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubject(request):
    id = request.user.id
    role = request.user.role.role
    if role == 'student':
        subjects = Subject.objects.filter(level=request.user.role.level)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    elif role == 'doctor':
        subjects = Subject.objects.filter(doctor=id)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    else:
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLevels(request):
    id = request.user.id
    role = request.user.role.role
    levels = []
    if role == "doctor":
        subjects = Subject.objects.filter(doctor=id)
        for i in range(len(subjects)):
            levels.append(subjects[i].level)
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data)

    elif role == 'admin':
        levels = Level.objects.all()
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data)
    else:
        return Response("only doctors and admins can user this route")

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLevelSubjects(request, level):
    id = request.user.id
    role = request.user.role.role
    if role == "doctor":
        subjects = Subject.objects.filter(doctor=id, level=level)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    elif role == "admin":
        subjects = Subject.objects.filter(level=level)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    else:
        return Response('only doctors and admins can user this route')

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response("user logged out")