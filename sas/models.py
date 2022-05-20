from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Level(models.Model):
    LEVELS = [
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
        ('Level 3', 'Level 3'),
        ('Level 4', 'Level 4')
    ]
    
    name = models.CharField(max_length=60, default=LEVELS[0][0], choices=LEVELS)
    
    def __str__(self):
        return self.name
    

class UserManager(BaseUserManager):
	def create_user(self, username, id, role, level=None, password=None,):
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			username=username,
            id=id,
            role= role,
            level=level
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, id, username, password, role='admin', level=None):
		user = self.create_user(
			id=self.normalize_email(id),
			password=password,
			username=username,
            role=role,
            level=level
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
    ROLES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('doctor', 'Doctor')
    ]
    
    id           = models.CharField(max_length=6, primary_key=True, unique=True)
    username 	 = models.CharField(max_length=14, unique=True)
    first_name   = models.CharField(max_length=60)
    last_name    = models.CharField(max_length=60)
    role         = models.CharField(choices=ROLES, default=ROLES[0][0], max_length=60)
    level        = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    date_joined	 = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login	 = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin	 = models.BooleanField(default=False)
    is_active	 = models.BooleanField(default=True)
    is_staff	 = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
	
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} {self.id}"

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    

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
        return f"{self.studentId.username} {self.subjectId.name}" 
