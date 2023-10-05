from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import User

# Create your models here.


class Organization(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    Logo = models.ImageField(
        upload_to='orgainizations/logos', blank=True, null=True)
    OrganizationName = models.CharField(
        _("OrgName"), blank=False, null=False, max_length=250)
    Description = models.TextField(_("description"))
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )
    Active = models.BooleanField(default=False)

    def __str__(self):
        return self.OrganizationName
