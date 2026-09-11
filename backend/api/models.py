from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
import uuid


class Student(models.Model):
    """Student profile model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    bio = models.TextField(blank=True, null=True)
    target_role = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('lead', 'Lead/Manager'),
        ],
        default='entry'
    )
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        ordering = ['-created_at']


class Resume(models.Model):
    """Resume upload and processing model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='resume')
    file = models.FileField(upload_to='resumes/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    extracted_text = models.TextField()
    skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    experience_years = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    education_level = models.CharField(
        max_length=100,
        choices=[
            ('hs', 'High School'),
            ('bachelors', "Bachelor's Degree"),
            ('masters', "Master's Degree"),
            ('phd', 'PhD'),
        ],
        blank=True
    )
    universities = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    processed = models.BooleanField(default=False)
    processing_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume for {self.student}"

    class Meta:
        ordering = ['-created_at']


class Project(models.Model):
    """GitHub projects linked to students"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    github_url = models.URLField()
    repository_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    languages = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    skills_demonstrated = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    analyzed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.repository_name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('student', 'github_url')


class JobPosting(models.Model):
    """Job postings for analysis"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    requirements = TextField()
    nice_to_have = models.TextField(blank=True)
    job_url = models.URLField(blank=True)
    source = models.CharField(
        max_length=50,
        choices=[
            ('linkedin', 'LinkedIn'),
            ('indeed', 'Indeed'),
            ('glassdoor', 'Glassdoor'),
            ('other', 'Other'),
        ]
    )
    required_skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    experience_years = models.IntegerField(default=0)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full-time', 'Full-Time'),
            ('part-time', 'Part-Time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
        ]
    )
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    posted_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ['-posted_date']


class SkillGapAnalysis(models.Model):
    """Skill gap analysis results"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='skill_gaps')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    missing_skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    partial_skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    matched_skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    gap_severity = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ]
    )
    fit_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    analysis_summary = models.TextField()
    recommendations = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gap Analysis: {self.student} vs {self.job_posting.title}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('student', 'job_posting')


class Skill(models.Model):
    """Skill definition model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('programming', 'Programming Language'),
            ('framework', 'Framework/Library'),
            ('database', 'Database'),
            ('tool', 'Tool/Platform'),
            ('soft', 'Soft Skill'),
            ('other', 'Other'),
        ]
    )
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ]
    )
    resource_links = models.JSONField(default=dict)  # {course_name: url}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']


class LearningPath(models.Model):
    """Personalized learning paths"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_paths')
    skill_gap_analysis = models.OneToOneField(
        SkillGapAnalysis, on_delete=models.CASCADE, related_name='learning_path'
    )
    target_role = models.CharField(max_length=255)
    duration_weeks = models.IntegerField()
    priority_level = models.CharField(
        max_length=50,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ]
    )
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Learning Path: {self.student} -> {self.target_role}"

    class Meta:
        ordering = ['-created_at']


class LearningActivityRecommendation(models.Model):
    """Recommended learning activities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_path = models.ForeignKey(
        LearningPath, on_delete=models.CASCADE, related_name='recommendations'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('course', 'Online Course'),
            ('book', 'Book'),
            ('project', 'Build Project'),
            ('tutorial', 'Tutorial'),
            ('documentation', 'Official Documentation'),
            ('practice', 'Practice Problem'),
            ('cert', 'Certification'),
        ]
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True)
    estimated_hours = models.IntegerField()
    difficulty = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    priority = models.IntegerField(default=0)  # 1-10, higher = more important
    source = models.CharField(max_length=100)  # Coursera, Udemy, etc.
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.skill.name})"

    class Meta:
        ordering = ['order_index', '-priority']


class LearningActivity(models.Model):
    """Tracked learning activities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_activities')
    recommendation = models.ForeignKey(
        LearningActivityRecommendation, on_delete=models.CASCADE, related_name='activities'
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('paused', 'Paused'),
        ],
        default='not_started'
    )
    hours_completed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.recommendation.title}"

    class Meta:
        ordering = ['-updated_at']


class ProgressMetric(models.Model):
    """Track student progress over time"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_metrics')
    metric_date = models.DateField()
    skills_acquired = models.IntegerField(default=0)
    skills_in_progress = models.IntegerField(default=0)
    average_fit_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_learning_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activities_completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress for {self.student} on {self.metric_date}"

    class Meta:
        ordering = ['-metric_date']
        unique_together = ('student', 'metric_date')
