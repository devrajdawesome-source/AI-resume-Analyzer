from rest_framework import serializers

class ResumeUploadSerializer(serializers.Serializer):
    resume = serializers.FileField(help_text="Upload your PDF resume")
    job_description = serializers.CharField(
        style={'base_template': 'textarea.html'}, 
        required=False, 
        allow_blank=True,
        help_text="Paste the job description here"
    )