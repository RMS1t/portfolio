from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class SNPValidator(validators.RegexValidator):
    """
     regular expression  for  cyrillic 3 words in username field
    """

    regex = r"^[а-яА-Я-]+\s[а-яА-Я-]+\s[а-яА-Я-]+$"
    message = _(
        "Enter a valid surname, name and patronymic. This value may contain only  cyrillic letters and '-'."
    )

@deconstructible
class LoginValidator(validators.RegexValidator):
    """
     regular expression  for 1 latin word in login field
    """

    regex = r"^[a-zA-Z-]+$"
    message = _(
        "Enter a valid login. This value may contain only  latin letters and '-'."
    )