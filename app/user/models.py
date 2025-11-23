from django.db import models

from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        
        user = self.model(email = email, password = password, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = description = models.TextField()

    def __str__(self):
        return f"{self.name}"


ROLE_LEVEL = {
    "Гость": 0,
    "Менеджер": 1,
    "Программист": 2,
    "Специалист технической поддержки": 3,
    "Администратор": 4,
    "Директор": 5
}

def assign_role_level(role_name):
    return ROLE_LEVEL.get(role_name, 0)


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    level = models.PositiveIntegerField(default = 0)

    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        self.level = assign_role_level(self.name)
        super().save(*args, **kwargs)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length = 100, verbose_name = 'Имя')
    last_name = models.CharField(max_length = 100, verbose_name = 'Фамилия')
    surname = models.CharField(max_length = 100, verbose_name = 'Отчество')

    email = models.EmailField(
        max_length = 100, 
        db_index = True, 
        blank = True, 
        unique=True,
        validators = [EmailValidator], 
        verbose_name = 'Электронная почта',
    )

    is_active = models.BooleanField(default=True)

    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=0, related_name='users')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.surname}"
    
    def has_permission(self, permission_name):
        return self.role.permissions.filter(name=permission_name).exists()
    

class UserRefreshToken(models.Model):
    refresh_token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refresh_tokens")

