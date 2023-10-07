from django.contrib import admin
from .models import Organization, Member
from django.utils.html import format_html


#------------------organization profile displayed in django admin panel-----------------
class OrganizationProfile(admin.ModelAdmin):
    # to avoid the error of the image field i.e The 'photo' attribute has no file associated with it. we passed it into a try/catch
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.Logo.url))
        except:
            pass  # just ingnore

    thumbnail.short_description = 'Organization Logo'
    list_display = ('thumbnail', 'user', 'OrganizationName',
                    'Description', 'phone_number', 'Active', 'InvitationLink',)
    list_display_links = ('thumbnail', 'user', 'OrganizationName')
    ordering = ('-user',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



#------------------organization's members profile displayed in django admin panel-----------------
class MembersProfile(admin.ModelAdmin):
    # to avoid the error of the image field i.e The 'photo' attribute has no file associated with it. we passed it into a try/catch
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.profile_picture.url))
        except:
            pass  # just ignore

    thumbnail.short_description = ' Profile Picture'
    list_display = ('thumbnail', 'user', 'MentoringRole',
                    'country', 'created_at', 'last_login')
    list_display_links = ('user',)
    readonly_fields = ('created_at', 'modified_at')
    ordering = ('-created_at',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Organization, OrganizationProfile)
admin.site.register(Member, MembersProfile)
