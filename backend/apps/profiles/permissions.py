from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Permission class for students"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'STUDENT'
        )


class IsMentor(permissions.BasePermission):
    """Permission class for mentors"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'MENTOR'
        )


class IsFloorWing(permissions.BasePermission):
    """Permission class for floor wings"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'FLOOR_WING'
        )


class IsAdmin(permissions.BasePermission):
    """Permission class for admins"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'ADMIN'
        )


class IsFloorWingOrAdmin(permissions.BasePermission):
    """Permission class for floor wings or admins"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role in ['FLOOR_WING', 'ADMIN']
        )


class IsMentorOrFloorWing(permissions.BasePermission):
    """Permission class for mentors or floor wings"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role in ['MENTOR', 'FLOOR_WING']
        )


class SameCampusPermission(permissions.BasePermission):
    """Ensure user can only access data from their campus"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return False
        
        user_profile = request.user.profile
        
        # Admin can access all campuses
        if user_profile.role == 'ADMIN':
            return True
        
        # Get object's campus
        obj_campus = None
        if hasattr(obj, 'campus'):
            obj_campus = obj.campus
        elif hasattr(obj, 'profile') and hasattr(obj.profile, 'campus'):
            obj_campus = obj.profile.campus
        
        # Check campus match
        return obj_campus == user_profile.campus


class SameFloorPermission(permissions.BasePermission):
    """Ensure user can only access data from their floor"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return False
        
        user_profile = request.user.profile
        
        # Admin and Floor Wing can access their floor
        if user_profile.role in ['ADMIN', 'FLOOR_WING']:
            # Admin needs campus context, Floor Wing needs exact floor match
            if user_profile.role == 'FLOOR_WING':
                obj_floor = None
                if hasattr(obj, 'floor'):
                    obj_floor = obj.floor
                elif hasattr(obj, 'profile') and hasattr(obj.profile, 'floor'):
                    obj_floor = obj.profile.floor
                
                return obj_floor == user_profile.floor
            return True
        
        # Mentors can only see their assigned students
        if user_profile.role == 'MENTOR':
            # Check if object is a student assigned to this mentor
            if hasattr(obj, 'profile') and hasattr(obj.profile, 'assigned_mentor'):
                return obj.profile.assigned_mentor == request.user
        
        return False
