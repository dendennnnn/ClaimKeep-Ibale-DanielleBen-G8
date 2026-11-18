from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CONSUMER = 'CONSUMER', 'Consumer (Registered User)'
        ADMIN = 'ADMIN', 'System Administrator'

    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CONSUMER,
    )
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def id(self):
        return self.user_id

    def is_consumer(self):
        return self.role == self.Role.CONSUMER

    def is_system_admin(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.full_name} ({self.email})"