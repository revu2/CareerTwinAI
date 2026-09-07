from typing import Dict, Any, List
from ..models.profile import StudentProfile

SAMPLE_PROFILES: Dict[str, StudentProfile] = {
    "revathi_ai": StudentProfile(
        id="revathi_ai",
        name="Revathi",
        degree="B.Tech",
        branch="Computer Science Engineering",
        year_of_study="3rd Year (Graduating 2026)",
        cgpa=8.6,
        current_skills=["Python", "SQL", "HTML", "CSS", "JavaScript"],
        projects=[
            "Personal Web Development Portfolio (Responsive HTML/CSS/JavaScript with project showcases)",
            "Student Performance & Grade Predictor (Python, Pandas, Scikit-Learn data modeling exploratory script)"
        ],
        certifications=[
            "Python Programming Fundamentals (Coursera)",
            "Relational Database Foundations & SQL Basics"
        ],
        career_interests=[
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning",
            "Generative AI & LLM Systems"
        ],
        target_career="AI Engineer",
        dream_company="Google / Microsoft / High-Growth AI Labs",
        readiness_score=48.0
    ),
    "demo_student": StudentProfile(
        id="demo_student",
        name="Revathi",
        degree="B.Tech",
        branch="Computer Science Engineering",
        year_of_study="3rd Year (Graduating 2026)",
        cgpa=8.6,
        current_skills=["Python", "SQL", "HTML", "CSS", "JavaScript"],
        projects=[
            "Personal Web Development Portfolio (Responsive HTML/CSS/JavaScript with project showcases)",
            "Student Performance & Grade Predictor (Python, Pandas, Scikit-Learn data modeling exploratory script)"
        ],
        certifications=[
            "Python Programming Fundamentals (Coursera)",
            "Relational Database Foundations & SQL Basics"
        ],
        career_interests=[
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning"
        ],
        target_career="AI Engineer",
        dream_company="Google / Microsoft / AI Labs",
        readiness_score=48.0
    ),
    "alex_ai": StudentProfile(
        id="alex_ai",
        name="Alex Chen",
        degree="B.S. in Computer Science",
        branch="Artificial Intelligence",
        year_of_study="4th Year (Senior)",
        cgpa=3.85,
        current_skills=["Python", "PyTorch", "FastAPI", "SQL", "Docker", "Git", "Scikit-Learn"],
        projects=[
            "NeuroDoc: Multimodal Clinical RAG Assistant (FastAPI, PyTorch, ChromaDB)",
            "VisionGuard: Edge Object Detection (PyTorch, YOLOv8, OpenCV)"
        ],
        certifications=[
            "Deep Learning Specialization (DeepLearning.AI)",
            "AWS Certified Cloud Practitioner"
        ],
        career_interests=["Deep Learning", "Computer Vision", "LLMs"],
        target_career="AI Engineer",
        dream_company="OpenAI / Scale AI / Google DeepMind",
        readiness_score=78.0
    ),
    "sarah_fullstack": StudentProfile(
        id="sarah_fullstack",
        name="Sarah Lin",
        degree="B.Tech",
        branch="Information Technology",
        year_of_study="3rd Year",
        cgpa=8.4,
        current_skills=["JavaScript", "TypeScript", "React", "Node.js", "Express", "HTML/CSS", "PostgreSQL"],
        projects=[
            "CollabCanvas: Multiplayer Whiteboard (React, WebSockets, Canvas API)",
            "DevPulse: Team Velocity Dashboard (Next.js, Tailwind, Prisma)"
        ],
        certifications=["Meta Front-End Developer Professional Certificate"],
        career_interests=["Fullstack Web Development", "Cloud Architecture", "UI/UX"],
        target_career="Fullstack Software Engineer",
        dream_company="Vercel / Stripe / Airbnb",
        readiness_score=72.0
    )
}

def get_sample_profile(profile_id: str = "revathi_ai") -> StudentProfile:
    if profile_id in SAMPLE_PROFILES:
        return SAMPLE_PROFILES[profile_id]
    return next(iter(SAMPLE_PROFILES.values()))
