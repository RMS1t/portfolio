# Импортируем необходимый функционал для создания кастомного валидатора
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class SNPValidator(validators.RegexValidator):
    regex = r"^[\w]+\s{3}$"
    message = _(
        "Enter a valid surname, name and patronymic. This value may contain only letters."
    )