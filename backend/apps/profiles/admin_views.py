from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Count, Q
from apps.profiles.models import UserProfile
from apps.profiles.permissions import IsAdmin
from apps.clt.models import CLTSubmission
from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission
from apps.iipc.models import LinkedInPostVerification, LinkedInConnectionVerification
from apps.scd.models import LeetCodeProfile


class AdminCampusOverviewView(APIView):
    """Admin view to see campus-level overview"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, campus):
        if campus not in ['TECH', 'ARTS']:
            return Response({
                'error': 'Invalid campus. Must be TECH or ARTS'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Determine floor range and campus name based on campus
        if campus == 'TECH':
            floors = [1, 2, 3, 4]
            campus_name = 'SNS College of Technology'
        elif campus == 'ARTS':
            floors = [1, 2, 3]
            campus_name = 'Dr. SNS Rajalakshmi College of Arts and Science'
        else:
            floors = []
            campus_name = ''
        
        floor_data = []
        for floor_num in floors:
            # Get counts for this floor
            students_count = UserProfile.objects.filter(
                role='STUDENT',
                campus=campus,
                floor=floor_num
            ).count()
            
            mentors_count = UserProfile.objects.filter(
                role='MENTOR',
                campus=campus,
                floor=floor_num
            ).count()
            
            floor_wing = UserProfile.objects.filter(
                role='FLOOR_WING',
                campus=campus,
                floor=floor_num
            ).select_related('user').first()
            
            floor_wing_name = None
            if floor_wing:
                floor_wing_name = f"{floor_wing.user.first_name} {floor_wing.user.last_name}"
            
            # Calculate submission stats (placeholder - implement based on your models)
            submission_stats = self._get_floor_submission_stats(campus, floor_num)
            
            # Floor name logic: TECH = Floor X, ARTS = Xst/nd/rd Year
            if campus == 'TECH':
                floor_name = f"Floor {floor_num}"
            else:
                if floor_num == 1:
                    floor_name = "1st Year"
                elif floor_num == 2:
                    floor_name = "2nd Year"
                elif floor_num == 3:
                    floor_name = "3rd Year"
                else:
                    floor_name = f"{floor_num}th Year"
            floor_data.append({
                'floor': floor_num,
                'floor_name': floor_name,
                'total_students': students_count,
                'total_mentors': mentors_count,
                'floor_wing': floor_wing_name,
                'floor_wing_id': floor_wing.user.id if floor_wing else None,
                'submissions': submission_stats
            })
        
        return Response({
            'campus': campus,
            'campus_name': campus_name,
            'floors': floor_data
        }, status=status.HTTP_200_OK)
    
    def _get_floor_submission_stats(self, campus, floor):
        """Get submission statistics for a floor - real implementation"""
        # Get all students on this floor
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus,
            floor=floor
        ).select_related('user')
        
        user_ids = [s.user.id for s in students]
        
        total = pending = approved = rejected = 0
        
        # CLT
        try:
            clt_qs = CLTSubmission.objects.filter(user_id__in=user_ids)
            total += clt_qs.count()
            pending += clt_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += clt_qs.filter(status='approved').count()
            rejected += clt_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # CFC - Hackathon
        try:
            hack_qs = HackathonSubmission.objects.filter(user_id__in=user_ids)
            total += hack_qs.count()
            pending += hack_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += hack_qs.filter(status='approved').count()
            rejected += hack_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # CFC - BMC
        try:
            bmc_qs = BMCVideoSubmission.objects.filter(user_id__in=user_ids)
            total += bmc_qs.count()
            pending += bmc_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += bmc_qs.filter(status='approved').count()
            rejected += bmc_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # CFC - Internship
        try:
            intern_qs = InternshipSubmission.objects.filter(user_id__in=user_ids)
            total += intern_qs.count()
            pending += intern_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += intern_qs.filter(status='approved').count()
            rejected += intern_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # CFC - GenAI
        try:
            genai_qs = GenAIProjectSubmission.objects.filter(user_id__in=user_ids)
            total += genai_qs.count()
            pending += genai_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += genai_qs.filter(status='approved').count()
            rejected += genai_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # IIPC - LinkedIn Post
        try:
            post_qs = LinkedInPostVerification.objects.filter(user_id__in=user_ids)
            total += post_qs.count()
            pending += post_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += post_qs.filter(status='approved').count()
            rejected += post_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # IIPC - LinkedIn Connection
        try:
            conn_qs = LinkedInConnectionVerification.objects.filter(user_id__in=user_ids)
            total += conn_qs.count()
            pending += conn_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            approved += conn_qs.filter(status='approved').count()
            rejected += conn_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        # Calculate progress percentage
        progress_percentage = 0
        if total > 0:
            progress_percentage = int((approved / total) * 100)
        
        return {
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'progress_percentage': progress_percentage
        }


class AdminFloorDetailView(APIView):
    """Admin view for detailed floor information"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, campus, floor):
        if campus not in ['TECH', 'ARTS']:
            return Response({
                'error': 'Invalid campus'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate floor range
        if campus == 'TECH' and floor not in [1, 2, 3, 4]:
            return Response({
                'error': 'Tech campus only has floors 1-4'
            }, status=status.HTTP_400_BAD_REQUEST)
        if campus == 'ARTS' and floor not in [1, 2, 3]:
            return Response({
                'error': 'Arts campus only has floors 1-3'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get floor wing
        floor_wing = UserProfile.objects.filter(
            role='FLOOR_WING',
            campus=campus,
            floor=floor
        ).select_related('user').first()
        
        # Get mentors on this floor
        mentors = UserProfile.objects.filter(
            role='MENTOR',
            campus=campus,
            floor=floor
        ).select_related('user')
        
        mentor_data = []
        for mentor_profile in mentors:
            # Count students assigned to this mentor on this floor
            student_count = UserProfile.objects.filter(
                role='STUDENT',
                campus=campus,
                floor=floor,
                assigned_mentor=mentor_profile.user
            ).count()
            
            mentor_data.append({
                'id': mentor_profile.user.id,
                'name': f"{mentor_profile.user.first_name} {mentor_profile.user.last_name}",
                'email': mentor_profile.user.email,
                'assigned_students': student_count
            })
        
        # Get students
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus,
            floor=floor
        ).select_related('user', 'assigned_mentor')
        
        student_data = []
        for student_profile in students:
            mentor_name = None
            if student_profile.assigned_mentor:
                mentor = student_profile.assigned_mentor
                mentor_name = f"{mentor.first_name} {mentor.last_name}"
            
            # Get real submission count for this student
            submission_count = self._get_student_submission_count(student_profile.user)
            
            student_data.append({
                'id': student_profile.user.id,
                'name': f"{student_profile.user.first_name} {student_profile.user.last_name}",
                'email': student_profile.user.email,
                'mentor': mentor_name,
                'mentor_id': student_profile.assigned_mentor.id if student_profile.assigned_mentor else None,
                'submissions': submission_count
            })
        
        floor_wing_data = None
        if floor_wing:
            floor_wing_data = {
                'id': floor_wing.user.id,
                'name': f"{floor_wing.user.first_name} {floor_wing.user.last_name}",
                'email': floor_wing.user.email
            }
        
        return Response({
            'campus': campus,
            'floor': floor,
            'floor_wing': floor_wing_data,
            'mentors': mentor_data,
            'students': student_data,
            'stats': {
                'total_students': len(student_data),
                'total_mentors': len(mentor_data),
                'unassigned_students': sum(1 for s in student_data if not s['mentor_id'])
            }
        }, status=status.HTTP_200_OK)
    
    def _get_student_submission_count(self, user):
        """Get total submission count for a student across all pillars"""
        count = 0
        
        try:
            count += CLTSubmission.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += HackathonSubmission.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += BMCVideoSubmission.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += InternshipSubmission.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += GenAIProjectSubmission.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += LinkedInPostVerification.objects.filter(user=user).count()
        except Exception:
            pass
        
        try:
            count += LinkedInConnectionVerification.objects.filter(user=user).count()
        except Exception:
            pass
        
        return count


class AdminAssignFloorWingView(APIView):
    """Admin endpoint to assign Floor Wing to a floor"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        campus = request.data.get('campus')
        floor = request.data.get('floor')
        user_id = request.data.get('user_id')
        
        if not all([campus, floor, user_id]):
            return Response({
                'error': 'campus, floor, and user_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            # Check if there's already a floor wing for this floor
            existing_floor_wing = UserProfile.objects.filter(
                role='FLOOR_WING',
                campus=campus,
                floor=floor
            ).exclude(user=user).first()
            
            if existing_floor_wing:
                return Response({
                    'error': f'Floor {floor} already has a Floor Wing assigned'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update user profile
            profile.role = 'FLOOR_WING'
            profile.campus = campus
            profile.floor = floor
            profile.save()
            
            return Response({
                'success': True,
                'message': f'{user.first_name} {user.last_name} assigned as Floor Wing for {campus} Floor {floor}'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)


class AdminAssignMentorView(APIView):
    """Admin endpoint to assign Mentor to a floor"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        campus = request.data.get('campus')
        floor = request.data.get('floor')
        user_id = request.data.get('user_id')
        
        if not all([campus, floor, user_id]):
            return Response({
                'error': 'campus, floor, and user_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            # Update user profile
            profile.role = 'MENTOR'
            profile.campus = campus
            profile.floor = floor
            profile.save()
            
            return Response({
                'success': True,
                'message': f'{user.first_name} {user.last_name} assigned as Mentor for {campus} Floor {floor}'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)


class AdminStudentDetailView(APIView):
    """Admin view to get detailed student information"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, student_id):
        try:
            user = User.objects.get(id=student_id)
            
            # Check if user has profile
            try:
                profile = user.profile
            except AttributeError:
                return Response({
                    'error': 'User profile not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Get mentor info
            mentor_info = None
            try:
                if hasattr(profile, 'assigned_mentor') and profile.assigned_mentor:
                    mentor = profile.assigned_mentor
                    mentor_info = {
                        'id': mentor.id,
                        'name': f"{mentor.first_name} {mentor.last_name}",
                        'email': mentor.email
                    }
            except Exception as e:
                print(f"Error getting mentor info: {e}")
            
            # Get pillar progress
            pillar_details = {'overall': 0, 'pillars': {}}
            try:
                pillar_details = self._get_pillar_progress(profile)
            except Exception as e:
                print(f"Error getting pillar progress: {e}")
            
            # Get submission counts
            submission_stats = {'total': 0, 'approved': 0, 'pending': 0, 'rejected': 0}
            try:
                submission_stats = self._get_submission_stats(profile)
            except Exception as e:
                print(f"Error getting submission stats: {e}")
            
            # Get campus name safely
            campus_name = 'N/A'
            if profile.campus:
                campus_name = 'SNS College of Technology' if profile.campus == 'TECH' else 'Dr. SNS Rajalakshmi College of Arts and Science'
            
            # Get XP points safely (may not exist in profile)
            xp_points = 0
            try:
                xp_points = profile.xp_points if hasattr(profile, 'xp_points') else 0
            except Exception:
                xp_points = 0
            
            return Response({
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'username': user.username,
                'roll_no': user.username or 'N/A',
                'campus': profile.campus or 'N/A',
                'campus_name': campus_name,
                'floor': profile.floor or 'N/A',
                'role': profile.role,
                'assigned_mentor': mentor_info,
                'pillar_progress': pillar_details.get('overall', 0),
                'pillar_details': pillar_details.get('pillars', {}),
                'submission_stats': submission_stats,
                'xp_points': xp_points,
                'status': self._get_student_status(pillar_details.get('overall', 0))
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'Student not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            print(f"AdminStudentDetailView Error: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'error': f'Error loading student details: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_pillar_progress(self, profile):
        """Calculate pillar progress - real implementation"""
        user = profile.user
        pillar_percentages = {}
        
        # CFC - 4 tasks (hackathon, BMC, internship, GenAI)
        try:
            cfc_completed = (
                HackathonSubmission.objects.filter(user=user, status='approved').count() +
                BMCVideoSubmission.objects.filter(user=user, status='approved').count() +
                InternshipSubmission.objects.filter(user=user, status='approved').count() +
                GenAIProjectSubmission.objects.filter(user=user, status='approved').count()
            )
            pillar_percentages['CFC'] = min(100, int((cfc_completed / 4) * 100))
        except Exception:
            pillar_percentages['CFC'] = 0
        
        # CLT - 1 certificate
        try:
            clt_completed = CLTSubmission.objects.filter(user=user, status='approved').count()
            pillar_percentages['CLT'] = min(100, clt_completed * 100)
        except Exception:
            pillar_percentages['CLT'] = 0
        
        # IIPC - 2 tasks (LinkedIn post + connection)
        try:
            iipc_completed = (
                LinkedInPostVerification.objects.filter(user=user, status='approved').count() +
                LinkedInConnectionVerification.objects.filter(user=user, status='approved').count()
            )
            pillar_percentages['IIPC'] = min(100, int((iipc_completed / 2) * 100))
        except Exception:
            pillar_percentages['IIPC'] = 0
        
        # SCD - 1 LeetCode profile with 10+ problems
        try:
            scd_profile = LeetCodeProfile.objects.filter(user=user, total_solved__gte=10).exists()
            pillar_percentages['SCD'] = 100 if scd_profile else 0
        except Exception:
            pillar_percentages['SCD'] = 0
        
        # SRI - not implemented yet
        pillar_percentages['SRI'] = 0
        
        # Calculate overall progress
        overall = int(sum(pillar_percentages.values()) / len(pillar_percentages)) if pillar_percentages else 0
        
        return {
            'overall': overall,
            'pillars': pillar_percentages
        }
    
    def _get_submission_stats(self, profile):
        """Get submission statistics - real implementation"""
        user = profile.user
        total = approved = pending = rejected = 0
        
        try:
            # CLT
            clt_qs = CLTSubmission.objects.filter(user=user)
            total += clt_qs.count()
            approved += clt_qs.filter(status='approved').count()
            pending += clt_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += clt_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # CFC - Hackathon
            hack_qs = HackathonSubmission.objects.filter(user=user)
            total += hack_qs.count()
            approved += hack_qs.filter(status='approved').count()
            pending += hack_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += hack_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # CFC - BMC
            bmc_qs = BMCVideoSubmission.objects.filter(user=user)
            total += bmc_qs.count()
            approved += bmc_qs.filter(status='approved').count()
            pending += bmc_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += bmc_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # CFC - Internship
            intern_qs = InternshipSubmission.objects.filter(user=user)
            total += intern_qs.count()
            approved += intern_qs.filter(status='approved').count()
            pending += intern_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += intern_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # CFC - GenAI
            genai_qs = GenAIProjectSubmission.objects.filter(user=user)
            total += genai_qs.count()
            approved += genai_qs.filter(status='approved').count()
            pending += genai_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += genai_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # IIPC - LinkedIn Post
            post_qs = LinkedInPostVerification.objects.filter(user=user)
            total += post_qs.count()
            approved += post_qs.filter(status='approved').count()
            pending += post_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += post_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        try:
            # IIPC - LinkedIn Connection
            conn_qs = LinkedInConnectionVerification.objects.filter(user=user)
            total += conn_qs.count()
            approved += conn_qs.filter(status='approved').count()
            pending += conn_qs.filter(status__in=['draft', 'submitted', 'under_review']).count()
            rejected += conn_qs.filter(status='rejected').count()
        except Exception:
            pass
        
        return {
            'total': total,
            'approved': approved,
            'pending': pending,
            'rejected': rejected
        }
    
    def _get_student_status(self, progress):
        """Determine student status based on progress"""
        if progress >= 80:
            return 'on_track'
        elif progress >= 50:
            return 'at_risk'
        else:
            return 'behind'


class AdminStatsView(APIView):
    """Admin dashboard stats view - real-time data"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        try:
            # Get all students count
            total_students = UserProfile.objects.filter(role='STUDENT').count()
            
            # Get all mentors count
            total_mentors = UserProfile.objects.filter(role='MENTOR').count()
            
            # Get all floor wings count (total floors with floor wings)
            total_floors = UserProfile.objects.filter(role='FLOOR_WING').values('campus', 'floor').distinct().count()
            
            # Get submission stats from all pillars - use try/except for each to handle missing models
            clt_pending = clt_approved = clt_rejected = 0
            try:
                clt_pending = CLTSubmission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                clt_approved = CLTSubmission.objects.filter(status='approved').count()
                clt_rejected = CLTSubmission.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            # CFC Submissions
            hackathon_pending = hackathon_approved = hackathon_rejected = 0
            bmc_pending = bmc_approved = bmc_rejected = 0
            internship_pending = internship_approved = internship_rejected = 0
            genai_pending = genai_approved = genai_rejected = 0
            
            try:
                hackathon_pending = HackathonSubmission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                hackathon_approved = HackathonSubmission.objects.filter(status='approved').count()
                hackathon_rejected = HackathonSubmission.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            try:
                bmc_pending = BMCVideoSubmission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                bmc_approved = BMCVideoSubmission.objects.filter(status='approved').count()
                bmc_rejected = BMCVideoSubmission.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            try:
                internship_pending = InternshipSubmission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                internship_approved = InternshipSubmission.objects.filter(status='approved').count()
                internship_rejected = InternshipSubmission.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            try:
                genai_pending = GenAIProjectSubmission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                genai_approved = GenAIProjectSubmission.objects.filter(status='approved').count()
                genai_rejected = GenAIProjectSubmission.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            # IIPC Submissions
            linkedin_post_pending = linkedin_post_approved = linkedin_post_rejected = 0
            linkedin_conn_pending = linkedin_conn_approved = linkedin_conn_rejected = 0
            
            try:
                linkedin_post_pending = LinkedInPostVerification.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                linkedin_post_approved = LinkedInPostVerification.objects.filter(status='approved').count()
                linkedin_post_rejected = LinkedInPostVerification.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            try:
                linkedin_conn_pending = LinkedInConnectionVerification.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
                linkedin_conn_approved = LinkedInConnectionVerification.objects.filter(status='approved').count()
                linkedin_conn_rejected = LinkedInConnectionVerification.objects.filter(status='rejected').count()
            except Exception:
                pass
            
            # Aggregate totals
            total_pending = (clt_pending + hackathon_pending + bmc_pending + internship_pending + 
                           genai_pending + linkedin_post_pending + linkedin_conn_pending)
            total_approved = (clt_approved + hackathon_approved + bmc_approved + internship_approved + 
                            genai_approved + linkedin_post_approved + linkedin_conn_approved)
            total_rejected = (clt_rejected + hackathon_rejected + bmc_rejected + internship_rejected + 
                            genai_rejected + linkedin_post_rejected + linkedin_conn_rejected)
            
            # Simple active users count - students with any submissions
            active_users = 0
            try:
                # Get unique user IDs with any submission activity
                active_user_ids = set()
                
                for submission_qs in [
                    CLTSubmission.objects.values_list('user_id', flat=True),
                    HackathonSubmission.objects.values_list('user_id', flat=True),
                    BMCVideoSubmission.objects.values_list('user_id', flat=True),
                    InternshipSubmission.objects.values_list('user_id', flat=True),
                    GenAIProjectSubmission.objects.values_list('user_id', flat=True),
                    LinkedInPostVerification.objects.values_list('user_id', flat=True),
                    LinkedInConnectionVerification.objects.values_list('user_id', flat=True),
                ]:
                    try:
                        active_user_ids.update(submission_qs)
                    except Exception:
                        pass
                
                active_users = len(active_user_ids)
            except Exception:
                active_users = total_students  # Fallback
            
            return Response({
                'totalStudents': total_students,
                'totalMentors': total_mentors,
                'totalFloors': total_floors,
                'pendingSubmissions': total_pending,
                'approvedSubmissions': total_approved,
                'rejectedSubmissions': total_rejected,
                'activeUsers': active_users,
                'submissionsThisWeek': total_pending + total_approved + total_rejected,
                'xpGivenThisMonth': 0,
                'floorPerformanceScore': 0,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            print(f"AdminStatsView Error: {str(e)}")
            print(traceback.format_exc())
            
            # Return default values on error
            return Response({
                'totalStudents': 0,
                'totalMentors': 0,
                'totalFloors': 0,
                'pendingSubmissions': 0,
                'approvedSubmissions': 0,
                'rejectedSubmissions': 0,
                'activeUsers': 0,
                'submissionsThisWeek': 0,
                'xpGivenThisMonth': 0,
                'floorPerformanceScore': 0,
                'error': str(e)
            }, status=status.HTTP_200_OK)
