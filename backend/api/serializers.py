from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Student, Resume, Project, JobPosting, SkillGapAnalysis,
    Skill, LearningPath, LearningActivityRecommendation,
    LearningActivity, ProgressMetric
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'bio', 'target_role', 'experience_level',
            'github_url', 'linkedin_url', 'portfolio_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id', 'student', 'file', 'file_name', 'extracted_text',
            'skills', 'experience_years', 'education_level',
            'universities', 'processed', 'processing_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'extracted_text', 'processed', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'student', 'github_url', 'repository_name', 'owner',
            'description', 'languages', 'skills_demonstrated', 'stars',
            'forks', 'is_public', 'analyzed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'skills_demonstrated', 'analyzed', 'created_at', 'updated_at']


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'company', 'description', 'requirements',
            'nice_to_have', 'job_url', 'source', 'required_skills',
            'experience_years', 'location', 'job_type', 'salary_min',
            'salary_max', 'posted_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'required_skills', 'created_at', 'updated_at']


class SkillGapAnalysisSerializer(serializers.ModelSerializer):
    job_posting = JobPostingSerializer(read_only=True)

    class Meta:
        model = SkillGapAnalysis
        fields = [
            'id', 'student', 'job_posting', 'missing_skills', 'partial_skills',
            'matched_skills', 'gap_severity', 'fit_score', 'analysis_summary',
            'recommendations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'description', 'difficulty_level',
            'resource_links', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LearningActivityRecommendationSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = LearningActivityRecommendation
        fields = [
            'id', 'learning_path', 'skill', 'activity_type', 'title',
            'description', 'url', 'estimated_hours', 'difficulty',
            'priority', 'source', 'order_index', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LearningPathSerializer(serializers.ModelSerializer):
    recommendations = LearningActivityRecommendationSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = LearningPath
        fields = [
            'id', 'student', 'skill_gap_analysis', 'target_role',
            'duration_weeks', 'priority_level', 'is_active',
            'start_date', 'end_date', 'completion_percentage',
            'recommendations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LearningActivitySerializer(serializers.ModelSerializer):
    recommendation = LearningActivityRecommendationSerializer(read_only=True)

    class Meta:
        model = LearningActivity
        fields = [
            'id', 'student', 'recommendation', 'status', 'hours_completed',
            'completion_percentage', 'started_at', 'completed_at',
            'notes', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProgressMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressMetric
        fields = [
            'id', 'student', 'metric_date', 'skills_acquired',
            'skills_in_progress', 'average_fit_score',
            'total_learning_hours', 'activities_completed', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
