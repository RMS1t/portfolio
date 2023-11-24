from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension, FileExtensionValidator

from taskboard.validators import LoginValidator, SNPValidator



class AdvUser(AbstractUser):
    pd_agree = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Consent to data processing')
    login = models.CharField(
        verbose_name='Login',
        max_length=255,
        help_text=_("Login"),
        validators=[LoginValidator],
        unique=True,
    )
    username = models.CharField(
        verbose_name='SNP(Surname Name Patronymic)',
        max_length=255,
        help_text=_("Cyrillic Surname First Name Patronymic"),
        validators=[SNPValidator],
        unique=False,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )


    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.login

    class Meta(AbstractUser.Meta):
        pass


class OrderPetition(models.Model):
    """Model representing a Order."""

    class OrderStatus(models.TextChoices):
        NEW = "N", _("Новая заявка")
        PROCESSING = "W", _("Принято на обработку")
        FINISHED = "E", _("Выполнена")

        def __str__(self):
            return self.value[1]

    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(
        max_length=1000, help_text="Enter a  description of the yours order", blank=False)

    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True, blank=False)

    user_id = models.ForeignKey(
        'AdvUser', on_delete=models.SET_NULL, null=True, blank=False)

    order_time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.NEW)

    image = models.ImageField(upload_to='users/%Y/%m/%d/',
                              validators=[validate_image_file_extension,
                                          FileExtensionValidator(['bmp', 'jpg', 'jpeg', 'png'],
                                                                 message='Allowed datatypes:bmp,jpg,jpeg,png')])
    design_image = models.ImageField(upload_to='design/%Y/%m/%d/', blank=True,
                              validators=[validate_image_file_extension,
                                          FileExtensionValidator(['bmp', 'jpg', 'jpeg', 'png'],
                                                                 message='Allowed datatypes:bmp,jpg,jpeg,png')])
    comment= models.TextField(
        max_length=1000, help_text="Enter a  description of the yours order", blank=True)

    class Meta:
        ordering = ['title', 'status']

    def get_absolute_url(self):
        """Returns the url to access a particular book record."""
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Category(models.Model):
    """Model representing a Category (e.g. 3d, 2d, Picture, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the Category", blank=False, null=False)

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
