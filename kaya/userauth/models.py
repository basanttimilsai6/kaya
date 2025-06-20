from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError("The phone number is required.")
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not password:
            raise ValueError("Superuser must have a password.")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ("user", "USER"),
        ("moderator", "MODERATOR"),
        ("admin", "ADMIN"),
    )

    phone = models.CharField(max_length=15, unique=True)
    provider = models.CharField(max_length=50, null=True, blank=True)
    roles = models.CharField(choices=ROLES, max_length=10, default="user")
    is_blocked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    # Standard fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class UserDevice(models.Model):
    DEVICE_TYPES = (
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device')
    device_id = models.CharField(max_length=100, null=True, blank=True)
    fcm_token = models.CharField(max_length=1000)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_id']),
        ]

    def __str__(self):
        return f"{self.user.phone} - {self.device_type}"
