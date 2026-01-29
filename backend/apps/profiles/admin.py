from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile, FloorAnnouncement


# Custom User Creation Form with Email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address for login.'
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='Optional. First name of the user.'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='Optional. Last name of the user.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    min_num = 1
    max_num = 1
    
    fieldsets = (
        ('Role & Assignment', {
            'fields': ('role', 'campus', 'floor', 'assigned_mentor')
        }),
        ('Platform IDs', {
            'fields': ('leetcode_id', 'github_id', 'linkedin_id')
        }),
    )
    
    def get_queryset(self, request):
        """Ensure profile exists before displaying inline"""
        qs = super().get_queryset(request)
        return qs


# Extended User Admin with UserProfile inline
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role', 'get_campus', 'get_floor']
    list_filter = BaseUserAdmin.list_filter + ('profile__role', 'profile__campus', 'profile__floor')
    
    # Override add_fieldsets to include email and names
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else '-'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'
    
    def get_campus(self, obj):
        return obj.profile.get_campus_display() if hasattr(obj, 'profile') and obj.profile.campus else '-'
    get_campus.short_description = 'Campus'
    get_campus.admin_order_field = 'profile__campus'
    
    def get_floor(self, obj):
        return f"Floor {obj.profile.floor}" if hasattr(obj, 'profile') and obj.profile.floor else '-'
    get_floor.short_description = 'Floor'
    get_floor.admin_order_field = 'profile__floor'
    
    def save_model(self, request, obj, form, change):
        """Ensure user is saved first and prevent duplicate profile creation"""
        # Set flag to skip automatic profile creation by signal
        obj._profile_creation_skip = True
        super().save_model(request, obj, form, change)
        # Ensure profile exists (will be populated by inline)
        if not hasattr(obj, 'profile'):
            UserProfile.objects.get_or_create(user=obj)


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Standalone UserProfile admin (for quick edits)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'campus', 'floor', 'assigned_mentor', 'leetcode_id', 'github_id', 'linkedin_id', 'updated_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'leetcode_id', 'github_id', 'linkedin_id']
    list_filter = ['role', 'campus', 'floor', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user', 'assigned_mentor']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'campus', 'floor', 'assigned_mentor')
        }),
        ('Platform IDs', {
            'fields': ('leetcode_id', 'github_id', 'linkedin_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FloorAnnouncement)
class FloorAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'floor_wing', 'campus', 'floor', 'priority', 'status', 'created_at', 'read_count']
    search_fields = ['title', 'message', 'floor_wing__username']
    list_filter = ['campus', 'floor', 'priority', 'status', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'read_count']
    filter_horizontal = ['read_by']
    
    fieldsets = (
        ('Announcement Details', {
            'fields': ('floor_wing', 'title', 'message', 'priority', 'status')
        }),
        ('Scope', {
            'fields': ('campus', 'floor')
        }),
        ('Expiry', {
            'fields': ('expires_at',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'read_count', 'read_by'),
            'classes': ('collapse',)
        }),
    )
