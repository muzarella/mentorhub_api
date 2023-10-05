from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import User

# inherit from the user Model and creae profile for the members


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(
        upload_to='users/profile_pictures', blank=True, null=True)
    country = models.CharField(_("country"), blank=False,
                               null=False, max_length=250)
    state = models.CharField(_("state"), blank=False,
                             null=False, max_length=250)
    city = models.CharField(_("city"), blank=False, null=False, max_length=100)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11)
    Timezone = models.CharField(_("Timezone"), blank=False,
                                null=False, max_length=250)
    LinkedIn = models.CharField(_("LinkedIn"), blank=False,
                                null=False, max_length=250)
    ShortCV = models.TextField(blank=True, null=True)
    CurrentEmployment = models.CharField(_("CurrentEmployment"), blank=False,
                                         null=False, max_length=250)
    MentoringRole = models.CharField(
        max_length=250, blank=True, null=True)
    ModeofCommunication = models.CharField(
        max_length=250, blank=True, null=True)
    PreviousExperience = models.CharField(
        max_length=250, blank=True, null=True)
    DevelopmentAreas = models.TextField(blank=True, null=True)
    OtherAreas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.email

    # this code will remove previous image and replace it with a new if updated.
    def save(self, *args, **kwargs):
        try:
            this = Member.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture:
                this.profile_picture.delete()
        except:
            pass
        super(Member, self).save(*args, **kwargs)
