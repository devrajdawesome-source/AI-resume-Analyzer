import pypdf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import render

from .serializers import ResumeUploadSerializer, UserRegisterSerializer
from .utils import calculate_ats_score
from .models import ResumeAnalysis

def home_view(request):
    """Serves the main HTML page."""
    return render(request, 'analyzer/index.html')

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"status": "Healthy", "message": "Backend running successfully!"})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalyzeResumeView(APIView):
    permission_classes = [AllowAny] # Open to both Guests & Logged-in Users

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        job_description = serializer.validated_data.get('job_description', '')
        resume_file = serializer.validated_data['resume']

        try:
            # Extract PDF text in-memory
            reader = pypdf.PdfReader(resume_file)
            extracted_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

            # Call Gemini LLM analysis engine
            ats_result = calculate_ats_score(extracted_text, job_description)

            # Check if user is logged in via JWT token (request.user is populated automatically)
            current_user = request.user if request.user.is_authenticated else None

            # Save analysis to Database
            saved_record = ResumeAnalysis.objects.create(
                user=current_user, # Link user OR None for Guest
                file_name=resume_file.name,
                job_description=job_description,
                match_score=ats_result['match_score'],
                matching_skills=ats_result['matching_skills'],
                missing_skills=ats_result['missing_skills'],
                suggestions=ats_result.get('suggestions', [])
            )

            return Response({
                "status": "Success",
                "id": saved_record.id,
                "is_guest": current_user is None,
                "ats_analysis": ats_result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AnalysisHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # If logged in, fetch ONLY this user's records
        if request.user.is_authenticated:
            history = ResumeAnalysis.objects.filter(user=request.user).order_by('-created_at')
        else:
            # Guest mode: Return empty list or message encouraging login
            return Response({
                "history": [],
                "is_guest": True,
                "message": "Log in to save and view your personal analysis history!"
            })

        data = [{
            "id": h.id,
            "file_name": h.file_name,
            "match_score": h.match_score,
            "matching_skills": h.matching_skills,
            "missing_skills": h.missing_skills,
            "suggestions": h.suggestions,
            "created_at": h.created_at
        } for h in history]

        return Response({"history": data, "is_guest": False})