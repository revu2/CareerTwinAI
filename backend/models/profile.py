from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class StudentProfile(BaseModel):
    id: str = Field(default="default_student")
    name: str = Field(default="", description="Student full name, empty if not yet entered")
    degree: str = Field(default="B.Tech")
    branch: str = Field(default="Computer Science Engineering")
    year_of_study: str = Field(default="3rd Year")
    cgpa: Optional[float] = Field(default=8.0, ge=0.0, le=10.0)
    current_skills: List[str] = Field(default_factory=lambda: ["Python", "SQL", "HTML", "CSS", "JavaScript"])
    projects: List[str] = Field(default_factory=lambda: [
        "Web Development Portfolio Project",
        "Student Performance Predictor in Python"
    ])
    certifications: List[str] = Field(default_factory=lambda: [
        "Python Programming Fundamentals",
        "Relational Database Foundations & SQL Basics"
    ])
    career_interests: List[str] = Field(default_factory=lambda: [
        "Artificial Intelligence", "Machine Learning", "Deep Learning"
    ])
    target_career: str = Field(default="AI Engineer")
    dream_company: Optional[str] = Field(default="Top Tech / AI Labs")
    job_description: Optional[str] = Field(default="", description="Custom Job Description pasted by student")
    resume_filename: Optional[str] = Field(default="", description="Uploaded resume PDF filename")
    raw_resume_text: Optional[str] = Field(default="", description="Extracted resume text")
    readiness_score: float = Field(default=48.0, ge=0.0, le=100.0)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def get_display_name(self) -> str:
        """Returns the entered name or 'Student Candidate' if unentered."""
        return self.name.strip() if self.name and self.name.strip() else "Student Candidate"

    def get_twin_title(self) -> str:
        """Returns '[Name]'s Career Digital Twin' if name entered, else 'Your Career Digital Twin'."""
        if self.name and self.name.strip():
            return f"{self.name.strip()}'s Career Digital Twin"
        return "Your Career Digital Twin"

    def get_skills_list(self) -> List[str]:
        return [s.strip() for s in self.current_skills if s.strip()]
