from django.db import models
from django.contrib.auth.models import User # Django's built-in User model

class ResumeAnalysis(models.Model):
    # Foreign key link to User. null=True allows Guest analyses!
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analyses", null=True, blank=True)
    file_name = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True)
    match_score = models.IntegerField()
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        return f"{username} - {self.file_name} ({self.match_score}%)"