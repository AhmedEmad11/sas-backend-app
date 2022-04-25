from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Level(models.Model):
    LEVELS = [
        ('L1', 'Level 1'),
        ('L2', 'Level 2'),
        ('L3', 'Level 3'),
        ('L4', 'Level 4')
    ]
    
    name = models.CharField(max_length=60, default=LEVELS[0][0], choices=LEVELS)
    
    def __str__(self):
        return self.name
    
  
class Subject(models.Model):
    name = models.CharField(max_length=60)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.studentId.username

class Role(models.Model):
    ROLES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('doctor', 'Doctor')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, default=ROLES[0][0], max_length=60)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_role(sender, instance, created, **kwargs):
        if created:
            Role.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_role(sender, instance, **kwargs):
        print(instance)
        instance.role.save()
    
    @receiver(post_save, sender=User)
    def create_user_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
        
    def __str__(self):
        return f"{self.user.username} {self.id}"
