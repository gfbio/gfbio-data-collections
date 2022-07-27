import re
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


#class BaseUser(AbstractUser):
#    password = None,
#    first_name = None  # type: ignore
#    last_name = None  # type: ignore
    


class User(AbstractUser):
    """
    Default custom user model for Collection Service.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Service(User):
    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    origin = CharField(_("Origin"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    password = None # type: ignore
    password1 = None # type: ignore
    password2 = None # type: ignore
    name = None # type: ignore
    email = None # type: ignore

    def clean(self):
        self.set_unusable_password()
        if not re.match(r"^[\w\d\_]+(\:[\w\d\_]+)*$", self.origin):
            raise ValidationError(
                "The origin needs to consist of namespaces (letters, numbers, undescores),"
                + " optionally separated by colons.")

    def __str__(self) -> str:
        return self.origin
