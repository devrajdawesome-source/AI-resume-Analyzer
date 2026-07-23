import pypdf
from django.shortcuts import render  # <--- ADDED: To render HTML templates
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ResumeUploadSerializer
from .utils import calculate_ats_score
from .models import ResumeAnalysis

# --- ADDED: View to serve the Frontend Web UI ---
def home_view(request):
    """Renders the HTML Frontend UI."""
    return render(request, 'analyzer/index.html')


class HealthCheckView(APIView):
    """Simple health check endpoint."""
    def get(self, request):
        return Response({"status": "Django backend is running successfully!"})


class AnalyzeResumeView(APIView):
    """Endpoint to upload a PDF resume, compute ATS score, and save to DB."""
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ResumeUploadSerializer

    def get(self, request):
        return Response({
            "message": "Use the HTML Form below to upload a PDF resume!",
            "instructions": "Select a PDF file and optionally paste a job description."
        })

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        resume_file = serializer.validated_data['resume']
        job_description = serializer.validated_data.get('job_description', '')
        
        # Parse PDF text
        extracted_text = ""
        try:
            reader = pypdf.PdfReader(resume_file)
            for page in reader.pages:
                extracted_text += page.extract_text() or ""
        except Exception as e:
            return Response(
                {"error": f"Failed to read PDF file: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Compute ATS Score
        ats_result = calculate_ats_score(
            resume_text=extracted_text, 
            job_description_text=job_description
        )
        
        # Save to DB
        saved_record = ResumeAnalysis.objects.create(
            file_name=resume_file.name,
            job_description=job_description,
            match_score=ats_result['match_score'],
            matching_skills=ats_result['matching_skills'],
            missing_skills=ats_result['missing_skills'],
            suggestions=ats_result.get('suggestions', [])
        )
        
        return Response({
            "status": "Success",
            "db_id": saved_record.id,
            "file_name": saved_record.file_name,
            "ats_analysis": ats_result,
            "saved_at": saved_record.created_at
        })


class AnalysisHistoryView(APIView):
    """Endpoint to fetch past resume analysis records from SQL DB."""
    def get(self, request):
        records = ResumeAnalysis.objects.all().order_by('-created_at')
        
        data = [
            {
                "id": record.id,
                "file_name": record.file_name,
                "match_score": record.match_score,
                "matching_skills": record.matching_skills,
                "missing_skills": record.missing_skills,
                "created_at": record.created_at
            }
            for record in records
        ]
        
        return Response({
            "total_records": len(data),
            "history": data
        })