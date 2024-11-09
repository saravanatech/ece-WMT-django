# authentication/admin.py

from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.forms import BaseInlineFormSet
from django.http.request import HttpRequest
from .models import Branch, HomePageMessage, SiteMaintenance, UserActivity, UserProfile, ScreenAccess, UserSession

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('is_logged_in',)
    filter_horizontal = ('screens','vendor')

class RecentInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-pk')[:10]
        return queryset
    
class UserActivityInline(admin.TabularInline):
    model = UserActivity
    formset = RecentInlineFormSet
    extra = 0
    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        # Return a list of fields that should be read-only
        return [field.name for field in self.model._meta.get_fields()]


class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline, UserActivityInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        # Hide 'is_superuser' and 'is_staff' fields for non-superusers
        return ['is_superuser', 'is_staff', 'user_permissions']
        
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('user_permissions','is_superuser','is_staff')}),
    )


    filter_horizontal = ('user_permissions',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    inlines = []
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Exclude the is_nib field from the form if the user is not a superuser
            form.base_fields.pop('can_archieve', None)
        return form
    
    def get_readonly_fields(self, request: HttpRequest, obj: Union[Any,None] = ...) -> Union[List[str],Tuple[Any, ...]]:
        return ['is_logged_in']
    
    list_display = ['user','role', 'is_logged_in']
    search_fields = ['user__username','role']
    list_filter = ["is_logged_in"]
    filter_horizontal = ('screens','vendor')

admin.site.register(UserProfile, UserProfileAdmin)

class ScreenAccessAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in ScreenAccess._meta.fields]

admin.site.register(ScreenAccess, ScreenAccessAdmin)

class HomePageMessageAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in HomePageMessage._meta.fields]

admin.site.register(HomePageMessage, HomePageMessageAdmin)



class SiteMaintenanceAdmin(admin.ModelAdmin):
    list_per_page = 1
    list_display = [f.name for f in SiteMaintenance._meta.fields]

admin.site.register(SiteMaintenance, SiteMaintenanceAdmin)

class UserActivityAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_per_page = 50
    list_display = [f.name for f in UserActivity._meta.fields]
    list_filter = ["type"]


admin.site.register(UserActivity, UserActivityAdmin)

class UserSessionAdmin(admin.ModelAdmin):
    search_fields = ['user__username','user__profile__role']
    list_per_page = 50
    list_display = ('user', 'get_user_role', 'login_time', 'is_active')
    list_filter = ["is_active"]

    def get_user_role(self, obj):
        return obj.user.profile.role  # Access the related UserProfile role
    
    get_user_role.short_description = 'Role'
    

admin.site.register(UserSession, UserSessionAdmin)