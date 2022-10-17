from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    GenderChoice = [('others', 'Others'),('male', 'Male'),('female' ,'Female')]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(max_length=10,choices=GenderChoice, default='male')
    birthDate = models.DateField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=30, default="India")
    bio = models.TextField(max_length=500, default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum deserunt cum consectetur ratione quisquam accusamus ipsum, voluptates repellendus obcaecati? Minima?")
    followers = models.ManyToManyField('User', blank=True, related_name='following')
    verified = models.BooleanField(default=False)
    profilePictureUrl = models.URLField()
    coverPictureUrl = models.URLField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthDate', 'gender']

    objects = UserManager()


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
 
    def nFollowers(self):
        return self.followers.all().count()

    def nFollowing(self):
        return self.following.all().count()