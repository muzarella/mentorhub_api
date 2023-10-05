from django.contrib import admin
from .models import Organization
from django.utils.html import format_html


class MembersProfile(admin.ModelAdmin):
    # to avoid the error of the image field i.e The 'photo' attribute has no file associated with it. we passed it into a try/catch
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.logo.url))
        except:
            pass  # just ingnore

    thumbnail.short_description = 'Organization Logo'
    list_display = ('thumbnail', 'user', 'OrganizationName',
                    'Description', 'phone_number', 'Active')
    list_display_links = ('thumbnail', 'user', 'OrganizationName')
    ordering = ('-user',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Organization, MembersProfile)
