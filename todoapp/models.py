
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


###############################################################################################################################################


#################          Validations          ################# 

def validate_capitalized(value):
        if value != value.capitalize():
            raise ValidationError('Invalid (not capitalized) value: %(value)s',params={'value': value})
        
def only_char(value): 
    if value.isalpha()==False:
        raise ValidationError('int value not access')
    
def validate_age(value):
        if 0< value <= 100:
            return value
        raise ValidationError('Age not valid')   


###############################################################################################################################################

# User Manager
class UserManager(BaseUserManager):
    def _create_user(self, email, password,is_staff,is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, **extra_fields)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

 
 
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    firstname=models.CharField(max_length=100,validators=[only_char],null=True)
    lastname=models.CharField(max_length=100,validators=[only_char],null=True,)
    email = models.EmailField(unique=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email
    
    
TASK_STATUS = (
    ('1', 'selected'),
    ('2', 'notStarted'),
    ('3', 'inProgress'),
    ('4', 'completed')
    )
    
class TaskDetails(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plan_details')
    todo_task_id=models.CharField(max_length=200,blank=True)
    task = models.JSONField(default=list, null=True)
    wbs_id = models.CharField(max_length=50, null=True, default="WBSID")
    status = models.CharField(max_length=50, choices=TASK_STATUS, default="2")
    exported = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    # def __str__(self):
    #  return str(self.task['text'])
     



