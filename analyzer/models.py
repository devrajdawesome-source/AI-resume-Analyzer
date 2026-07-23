from django.db import models

class ResumeAnalysis(models.Model):
    file_name = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True)
    match_score = models.IntegerField()
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - Score: {self.match_score}% ({self.created_at.strftime('%Y-%m-%d %H:%M')})"