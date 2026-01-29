from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from apps.profiles.models import UserProfile
from apps.profiles.permissions import IsFloorWing
from apps.profiles.serializers import UserProfileSerializer


class FloorWingDashboardView(APIView):
    """Dashboard view for Floor Wing showing floor-level statistics"""
    permission_classes = [IsAuthenticated, IsFloorWing]
    
    def get(self, request):
        floor_wing_profile = request.user.profile
        campus = floor_wing_profile.campus
        floor = floor_wing_profile.floor
        
        if not campus or not floor:
            return Response({
                'error': 'Floor Wing must be assigned to a campus and floor'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all students on this floor
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus,
            floor=floor
        ).select_related('user', 'assigned_mentor')
        
        # Get all mentors on this floor
        mentors = UserProfile.objects.filter(
            role='MENTOR',
            campus=campus,
            floor=floor
        ).select_related('user')
        
        # Calculate mentor workload with detailed stats
        mentor_stats = []
        for mentor_profile in mentors:
            assigned_students = students.filter(assigned_mentor=mentor_profile.user)
            assigned_count = assigned_students.count()
            
            # Get submission stats for this mentor's students
            # This is a simplified version - expand based on your submission models
            pending_reviews = 0  # Implement based on submission model
            approval_rate = 0  # Calculate based on submissions
            
            # Determine workload status
            if assigned_count == 0:
                workload_status = 'low'
            elif assigned_count <= 5:
                workload_status = 'balanced'
            else:
                workload_status = 'overloaded'
            
            mentor_stats.append({
                'id': mentor_profile.user.id,
                'name': f"{mentor_profile.user.first_name} {mentor_profile.user.last_name}",
                'username': mentor_profile.user.username,
                'email': mentor_profile.user.email,
                'assigned_students': assigned_count,
                'assigned_students_count': assigned_count,  # For compatibility
                'pending_reviews': pending_reviews,
                'approval_rate': approval_rate,
                'workload_status': workload_status,
                'last_active': None  # Can be implemented with activity tracking
            })
        
        # Students without mentors
        unassigned_students = students.filter(assigned_mentor__isnull=True).count()
        assigned_students_count = students.filter(assigned_mentor__isnull=False).count()
        
        # Calculate average floor completion
        avg_completion = self._calculate_avg_completion(students)
        
        # Calculate pillar statistics
        pillar_stats = self._get_pillar_stats(campus, floor)
        
        # Get pending reviews count
        pending_reviews_total = 0  # Implement based on submission model
        
        return Response({
            'campus': campus,
            'campus_name': floor_wing_profile.get_campus_display(),
            'floor': floor,
            'floor_name': floor_wing_profile.get_floor_display(),
            'total_students': students.count(),
            'total_mentors': mentors.count(),
            'assigned_students': assigned_students_count,
            'unassigned_students': unassigned_students,
            'avg_floor_completion': avg_completion,
            'pending_mentor_reviews': pending_reviews_total,
            'mentor_stats': mentor_stats,
            'pillar_stats': pillar_stats
        }, status=status.HTTP_200_OK)
    
    def _calculate_avg_completion(self, students):
        """Calculate average completion rate for all students on floor"""
        # Placeholder - implement based on your submission tracking
        # This should calculate: (total completed pillars / (total students * 5 pillars)) * 100
        return 0
    
    def _get_pillar_stats(self, campus, floor):
        """Calculate pillar-wise statistics for the floor"""
        # This is a placeholder - implement based on your actual submission models
        return {
            'cfc': {'submitted': 0, 'approved': 0, 'pending': 0, 'rejected': 0, 'completion_rate': 0},
            'clt': {'submitted': 0, 'approved': 0, 'pending': 0, 'rejected': 0, 'completion_rate': 0},
            'sri': {'submitted': 0, 'approved': 0, 'pending': 0, 'rejected': 0, 'completion_rate': 0},
            'iipc': {'submitted': 0, 'approved': 0, 'pending': 0, 'rejected': 0, 'completion_rate': 0},
            'scd': {'submitted': 0, 'approved': 0, 'pending': 0, 'rejected': 0, 'completion_rate': 0},
        }



class FloorWingStudentsView(APIView):
    """View and manage students for Floor Wing"""
    permission_classes = [IsAuthenticated, IsFloorWing]
    
    def get(self, request):
        floor_wing_profile = request.user.profile
        campus = floor_wing_profile.campus
        floor = floor_wing_profile.floor
        
        # Get filter parameters
        filter_type = request.query_params.get('filter', 'all')  # all, unassigned, at_risk, low_progress
        
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus,
            floor=floor
        ).select_related('user', 'assigned_mentor')
        
        # Apply filters
        if filter_type == 'unassigned':
            students = students.filter(assigned_mentor__isnull=True)
        elif filter_type == 'at_risk':
            # Students with low progress - implement based on submission model
            pass
        elif filter_type == 'low_progress':
            # Students below certain completion threshold
            pass
        
        student_data = []
        for student_profile in students:
            mentor_name = None
            mentor_id = None
            if student_profile.assigned_mentor:
                mentor = student_profile.assigned_mentor
                mentor_name = f"{mentor.first_name} {mentor.last_name}"
                mentor_id = mentor.id
            
            # Calculate pillar progress for this student
            pillar_progress = self._get_student_pillar_progress(student_profile)
            pending_submissions = self._get_pending_submissions(student_profile)
            
            # Determine status
            completion_rate = pillar_progress.get('overall_completion', 0)
            if completion_rate >= 80:
                student_status = 'on_track'
            elif completion_rate >= 50:
                student_status = 'moderate'
            else:
                student_status = 'at_risk'
            
            student_data.append({
                'id': student_profile.user.id,
                'username': student_profile.user.username,
                'name': f"{student_profile.user.first_name} {student_profile.user.last_name}",
                'email': student_profile.user.email,
                'roll_no': student_profile.user.username,  # Assuming username is roll no
                'assigned_mentor_id': mentor_id,
                'assigned_mentor_name': mentor_name,
                'pillar_progress': pillar_progress.get('overall_completion', 0),
                'pending_submissions': pending_submissions,
                'status': student_status,
                'leetcode_id': student_profile.leetcode_id,
                'github_id': student_profile.github_id,
                'linkedin_id': student_profile.linkedin_id,
                'pillar_details': pillar_progress.get('pillars', {}),
            })
        
        return Response({
            'students': student_data,
            'total_count': len(student_data),
            'filter_applied': filter_type
        }, status=status.HTTP_200_OK)
    
    def _get_student_pillar_progress(self, student_profile):
        """Calculate pillar-wise progress for a student"""
        # Placeholder - implement based on your submission model
        return {
            'overall_completion': 0,
            'pillars': {
                'cfc': 0,
                'clt': 0,
                'sri': 0,
                'iipc': 0,
                'scd': 0
            }
        }
    
    def _get_pending_submissions(self, student_profile):
        """Get count of pending submissions for a student"""
        # Placeholder - implement based on your submission model
        return 0


class FloorWingMentorsView(APIView):
    """View mentors for Floor Wing"""
    permission_classes = [IsAuthenticated, IsFloorWing]
    
    def get(self, request):
        floor_wing_profile = request.user.profile
        campus = floor_wing_profile.campus
        floor = floor_wing_profile.floor
        
        # Get all students on this floor for workload calculation
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus,
            floor=floor
        ).select_related('assigned_mentor')
        
        mentors = UserProfile.objects.filter(
            role='MENTOR',
            campus=campus,
            floor=floor
        ).select_related('user')
        
        mentor_data = []
        for mentor_profile in mentors:
            assigned_students = students.filter(assigned_mentor=mentor_profile.user)
            assigned_count = assigned_students.count()
            
            # Get submission stats for this mentor's students
            pending_reviews = 0  # Implement based on submission model
            approval_rate = 0  # Calculate based on submissions
            
            # Determine workload status
            if assigned_count == 0:
                workload_status = 'low'
            elif assigned_count <= 5:
                workload_status = 'balanced'
            else:
                workload_status = 'overloaded'
            
            mentor_data.append({
                'id': mentor_profile.user.id,
                'username': mentor_profile.user.username,
                'name': f"{mentor_profile.user.first_name} {mentor_profile.user.last_name}",
                'email': mentor_profile.user.email,
                'assigned_students_count': assigned_count,
                'pending_reviews': pending_reviews,
                'approval_rate': approval_rate,
                'workload_status': workload_status,
                'last_active': None  # Can be implemented with activity tracking
            })
        
        return Response({
            'mentors': mentor_data,
            'total': len(mentor_data)
        }, status=status.HTTP_200_OK)


class FloorWingAssignStudentView(APIView):
    """Assign or reassign student to mentor"""
    permission_classes = [IsAuthenticated, IsFloorWing]
    
    def post(self, request):
        floor_wing_profile = request.user.profile
        campus = floor_wing_profile.campus
        floor = floor_wing_profile.floor
        
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')
        
        if not student_id or not mentor_id:
            return Response({
                'error': 'student_id and mentor_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verify student belongs to this floor
            student = User.objects.get(id=student_id)
            if (student.profile.role != 'STUDENT' or 
                student.profile.campus != campus or 
                student.profile.floor != floor):
                return Response({
                    'error': 'Student not found in your floor'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Verify mentor belongs to this floor
            mentor = User.objects.get(id=mentor_id)
            if (mentor.profile.role != 'MENTOR' or 
                mentor.profile.campus != campus or 
                mentor.profile.floor != floor):
                return Response({
                    'error': 'Mentor not found in your floor'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Assign mentor to student
            student.profile.assigned_mentor = mentor
            student.profile.save()
            
            return Response({
                'success': True,
                'message': f'Student assigned to {mentor.first_name} {mentor.last_name}'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
