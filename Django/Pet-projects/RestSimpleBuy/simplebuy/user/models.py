from django.contrib.auth.models import AbstractUser
from django.db import models
from user.validators import SNPValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MyUser(AbstractUser):
    username = models.CharField(
        verbose_name='SNP(Surname Name Patronymic)',
        max_length=255,
        help_text=_(
            "Required field. Enter Surname First Name Patronymic"
        ),
        validators=[SNPValidator],
        unique=False,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
