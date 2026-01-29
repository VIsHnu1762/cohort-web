from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
from datetime import datetime
import json
from apps.dashboard.models import Announcement


class JobInternshipListView(APIView):
    """
    Fetch job and internship announcements posted by mentors
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        opportunities = []
        
        # Fetch job/internship announcements from database
        announcements = Announcement.objects.filter(
            category__in=['job', 'internship']
        ).select_related('mentor').order_by('-created_at')
        
        for announcement in announcements:
            # Parse skills
            skills = []
            if announcement.required_skills:
                skills = [s.strip() for s in announcement.required_skills.split(',')][:3]
            
            opportunity = {
                'id': f'ann_{announcement.id}',
                'title': announcement.title,
                'company': announcement.company_name or 'Company',
                'location': announcement.job_location or 'Location TBA',
                'type': announcement.category,  # 'job' or 'internship'
                'mode': announcement.job_mode or 'on-site',
                'duration': announcement.job_duration or 'TBA',
                'stipend': announcement.job_stipend or 'Competitive',
                'posted_date': announcement.created_at.strftime('%Y-%m-%d'),
                'deadline': announcement.application_deadline.strftime('%b %d, %Y') if announcement.application_deadline else 'Open',
                'url': announcement.application_url or '#',
                'logo': 'https://via.placeholder.com/100x100?text=' + (announcement.company_name[:1] if announcement.company_name else 'C'),
                'description': announcement.description,
                'skills': skills,
                'experience': 'Freshers',
                'posted_by': f"{announcement.mentor.first_name} {announcement.mentor.last_name}".strip() or announcement.mentor.username
            }
            opportunities.append(opportunity)
        
        return Response({
            'success': True,
            'count': len(opportunities),
            'opportunities': opportunities
        }, status=status.HTTP_200_OK)
