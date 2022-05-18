from .serializers import (
    LevelSerializer, SubjectSerializer, UserSerializer
)

from .models import (
    Attendance,
    User,
    Level,
    Subject
)
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
        "GET AUTHED getLevelSubjects/<int:level>/": "get the subjects of a single level",
        "GET AUTHED getLevelStudents/<int:level>/": "get the students of a single level"
    }
    return Response(res)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLevelStudents(request, level):
    role = request.user.role
    if role == 'doctor' or role == 'admin':
        students = User.objects.filter(level=level)
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
    else:
        return Response("students can't use this route")
        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubjectAttendance(request, level, subject):
    id = request.user.id
    role = request.user.role
    subject = get_object_or_404(Subject, id=subject)
    if role == 'doctor':
        if subject.doctor.id == id:
            queryset = User.objects.filter(level=level)
            serializer = UserSerializer(queryset, many=True, context={'subjectId':subject.id})
            return Response(serializer.data)
        else:
            return Response("this doctor does not teach this subject")
    elif role == 'student':
        if subject.level == request.user.level:
            queryset = User.objects.filter(id=id)
            serializer = UserSerializer(queryset, many=True, context={'subjectId':subject.id})
            return Response(serializer.data)
        else:
            return Response("this student does not take this subject")
    else:
        queryset = User.objects.filter(level=level)
        serializer = UserSerializer(queryset, many=True, context={'subjectId':subject.id})
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def markAttendance(request):
    studentId = request.data["studentId"]
    subjectId = request.data["subjectId"]
    
    if request.user.role == "student":
        return Response("only doctors and admins can use this route")

    student = get_object_or_404(User, id=studentId)
    role = student.role
    if role == 'student':
        sub = get_object_or_404(Subject, id=subjectId)
        if sub.level == student.level:
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
    id = request.user.id
    query = User.objects.get(id=id)
    serializer = UserSerializer(query)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubjects(request):
    id = request.user.id
    role = request.user.role
    if role == 'student':
        subjects = Subject.objects.filter(level=request.user.level)
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
    role = request.user.role
    levels = []
    if role == "doctor":
        subjects = Subject.objects.filter(doctor=id)
        for i in range(len(subjects)):
            if subjects[i].level not in levels:
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
    role = request.user.role
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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createAttendanceForLevel(request):
    level = request.data["levelId"]
    role = request.user.role
    print(role)
    if role != "admin":
        return Response("only admins can use this route")
    
    subjects = Subject.objects.filter(level=level)
    students = User.objects.filter(level=level)
    
    counter = 0
    
    for student in students:
        for subject in subjects:
            attendance, created = Attendance.objects.get_or_create(subjectId=subject, studentId=student)
            if created:
                attendance.save()
                counter +=1
                
    return Response(f"created {counter} attendance object/s")
