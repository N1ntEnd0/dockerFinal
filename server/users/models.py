from django.contrib.auth import password_validation
from django.contrib.auth.models import UserManager as UManager, AbstractUser
from django.db import models, IntegrityError
from social_django.managers import UserSocialAuthManager as SocialAuthManager
from social_django.models import UserSocialAuth as SocialAuth, AbstractUserSocialAuth, DjangoStorage

from .utils import validate_credentials
# Create your models here.

class UserManager(UManager):

    def _create_user(self, username, email, password, **extra_fields):
        validate_credentials(username, email, password)
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):

    class Meta:
        db_table = 'user'
        permissions = (
            ("have_gdrive_permissions", "have a permissions for share folder"),
        )
        # constraints = [
        #     models.CheckConstraint(check=models.Q(username__=))
        # ]

class UserGoogleCredentials(models.Model):
    user = models.OneToOneField(User, related_name='user_credentials', on_delete=models.CASCADE)
    extra_data = models.JSONField()

    class Meta:
        db_table = 'user_g_credentials'


