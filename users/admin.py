# authentication/admin.py

from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.forms import BaseInlineFormSet
from django.http.request import HttpRequest
from .models import Branch, HomePageMessage, SiteMaintenance, UserActivity, UserProfile, ScreenAccess

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('is_logged_in',)

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
    
    filter_horizontal = ('branches', 'screens')
    list_display = ['user','role', 'is_logged_in']
    search_fields = ['user__username','role']
    list_filter = ["is_logged_in","is_sales","is_ho","is_nib","is_dmd"]

admin.site.register(UserProfile, UserProfileAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Branch._meta.fields]

admin.site.register(Branch, BranchAdmin)


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