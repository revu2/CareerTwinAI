from typing import Dict, Any, List, Set
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import ProfileAgentOutput, ReadinessScoreBreakdown
from ..data.role_benchmarks import get_role_benchmark
from ..services.resume_parser import extract_skills_from_text

class ProfileAgent(BaseAgent):
    """
    AGENT 1: DIGITAL TWIN / PROFILE AGENT

    Calculates a deterministic AI-Estimated Readiness Score based on:
    - 40% Required Skills (compared against target role & custom JD)
    - 25% Projects and Practical Experience
    - 15% Education and Certifications
    - 20% Role-Specific Skill Gaps & Alignment
    """

    def __init__(self):
        super().__init__(
            name="Digital Twin / Profile Agent",
            role_description=(
                "an intelligent career profile analyst that computes a deterministic "
                "AI-estimated readiness score by comparing a student's profile/resume "
                "against target career benchmarks and job descriptions."
            )
        )

    def analyze_profile(self, profile: StudentProfile) -> ProfileAgentOutput:
        # 1. Gather Student Skills (Lowercase Set)
        user_skills = [s.strip().lower() for s in profile.get_skills_list() if s.strip()]
        user_skill_set = set(user_skills)

        # 2. Get Standard Benchmark Skills for Target Role
        target_role = profile.target_career or "Software Engineer"
        benchmark = get_role_benchmark(target_role)
        core_benchmark_skills = list(benchmark.get("core_skills", []))
        important_benchmark_skills = list(benchmark.get("important_skills", []))

        # Check for clean initial empty state
        if not user_skills and not profile.projects and not profile.resume_filename:
            breakdown = ReadinessScoreBreakdown(
                required_skills_score=0.0,
                projects_experience_score=0.0,
                education_certs_score=0.0,
                role_gaps_score=0.0,
                total_score=0.0,
                matched_skills=[],
                missing_skills=core_benchmark_skills[:6],
                score_explanation="No resume or skills analyzed yet. Upload a PDF resume or enter skills above to calculate your deterministic readiness score.",
                improvement_recommendations=[
                    "Upload your PDF resume to parse skills, projects, and certifications automatically.",
                    "Select a target role or paste a Job Description (JD) to benchmark against specific job openings."
                ]
            )
            return ProfileAgentOutput(
                summary="Digital Twin is in a clean initial state. Upload your resume and select a target career role to calculate your AI readiness score.",
                strengths=["Ready to analyze your academic background, skills, and projects."],
                weaknesses=[f"Upload resume to benchmark against {target_role} standards."],
                career_stage="Initial Baseline / Awaiting Resume",
                readiness_estimate=0.0,
                breakdown=breakdown
            )
        
        # 3. Extract Additional Required Skills from custom JD if provided
        jd_skills: List[str] = []
        if profile.job_description and profile.job_description.strip():
            jd_skills = extract_skills_from_text(profile.job_description)

        # Combined unique list of required skills
        combined_required: List[str] = []
        for s in core_benchmark_skills + jd_skills + important_benchmark_skills:
            if s not in combined_required:
                combined_required.append(s)

        # Helper matching function
        def is_matched(req_skill: str) -> bool:
            req_lower = req_skill.lower().strip()
            for u in user_skills:
                if u == req_lower or u in req_lower or req_lower in u:
                    return True
            return False

        matched_skills: List[str] = []
        missing_skills: List[str] = []

        for req in combined_required:
            if is_matched(req):
                if req not in matched_skills:
                    matched_skills.append(req)
            else:
                if req not in missing_skills:
                    missing_skills.append(req)

        # -------------------------------------------------------------
        # 4. DETERMINISTIC 40 / 25 / 15 / 20 READINESS SCORE BREAKDOWN
        # -------------------------------------------------------------

        # A. 40% — Required Skills Match
        total_eval_skills = max(len(core_benchmark_skills) + (len(jd_skills) if jd_skills else 0), 1)
        skills_ratio = min(len(matched_skills) / total_eval_skills, 1.0)
        required_skills_score = round(skills_ratio * 40.0, 1)

        # B. 25% — Projects & Practical Experience
        project_count = len(profile.projects)
        project_score = 0.0
        if project_count >= 3:
            project_score = 25.0
        elif project_count == 2:
            project_score = 19.0
        elif project_count == 1:
            project_score = 12.0
        elif project_count == 0 and not user_skills:
            project_score = 0.0
        else:
            project_score = 4.0

        if profile.raw_resume_text:
            text_l = profile.raw_resume_text.lower()
            if "intern" in text_l or "internship" in text_l:
                project_score = min(project_score + 4.0, 25.0)
        projects_experience_score = round(project_score, 1)

        # C. 15% — Education & Certifications
        edu_score = 0.0
        deg_l = (profile.degree or "").lower()
        branch_l = (profile.branch or "").lower()
        if any(b in branch_l for b in ["computer", "ai", "artificial", "data", "information", "it", "software"]):
            edu_score += 8.0
        elif branch_l:
            edu_score += 5.0

        if profile.cgpa is not None:
            if profile.cgpa >= 8.5:
                edu_score += 3.0
            elif profile.cgpa >= 7.5:
                edu_score += 2.0
            elif profile.cgpa >= 6.5:
                edu_score += 1.0
        elif user_skills:
            edu_score += 2.0

        cert_count = len(profile.certifications)
        if cert_count >= 2:
            edu_score += 4.0
        elif cert_count == 1:
            edu_score += 2.5

        education_certs_score = round(min(edu_score, 15.0), 1)

        # D. 20% — Role-Specific Skill Gaps & Alignment
        missing_count = len(missing_skills)
        if missing_count <= 1:
            role_gaps_score = 20.0
        elif missing_count <= 3:
            role_gaps_score = 14.0
        elif missing_count <= 5:
            role_gaps_score = 9.0
        else:
            role_gaps_score = 5.0

        # Total Composite Readiness Score (Max 100.0)
        total_score = round(
            required_skills_score + projects_experience_score + education_certs_score + role_gaps_score,
            1
        )
        total_score = max(10.0, min(total_score, 98.0))

        # -------------------------------------------------------------
        # 5. EXPLANATION & RECOMMENDATIONS
        # -------------------------------------------------------------
        jd_note = " and custom Job Description" if profile.job_description and profile.job_description.strip() else ""
        explanation = (
            f"AI-Estimated Readiness Score of {total_score}% computed across 4 dimensions for {target_role}{jd_note}: "
            f"Required Skills ({required_skills_score}/40 pts), Projects & Practical Experience ({projects_experience_score}/25 pts), "
            f"Education & Certifications ({education_certs_score}/15 pts), and Role Gap Alignment ({role_gaps_score}/20 pts). "
            f"Found {len(matched_skills)} matched competencies and {len(missing_skills)} missing priority skills."
        )

        recommendations = []
        if missing_skills:
            recommendations.append(f"Master priority missing skills: {', '.join(missing_skills[:3])}.")
        if project_count < 3:
            recommendations.append("Build and deploy 1 additional production-grade portfolio project with cloud API serving.")
        if len(profile.certifications) < 2:
            recommendations.append(f"Earn a recognized industry specialization certificate in {target_role} tools.")
        if not recommendations:
            recommendations.append("Practice system design whiteboarding and mock technical interviews.")

        breakdown = ReadinessScoreBreakdown(
            required_skills_score=required_skills_score,
            projects_experience_score=projects_experience_score,
            education_certs_score=education_certs_score,
            role_gaps_score=role_gaps_score,
            total_score=total_score,
            matched_skills=matched_skills[:8],
            missing_skills=missing_skills[:8],
            score_explanation=explanation,
            improvement_recommendations=recommendations
        )

        # -------------------------------------------------------------
        # 6. STRENGTHS & WEAKNESSES
        # -------------------------------------------------------------
        strengths = []
        if matched_skills:
            strengths.append(f"Strong match in core role competencies: {', '.join(matched_skills[:4])}.")
        if project_count >= 2:
            strengths.append(f"Demonstrates practical hands-on capability with {project_count} listed projects.")
        if profile.cgpa and profile.cgpa >= 8.0:
            strengths.append(f"Strong academic record ({profile.cgpa} CGPA in {profile.branch}).")
        if not strengths:
            strengths.append("Foundational academic background with growth potential.")

        weaknesses = []
        if missing_skills:
            weaknesses.append(f"Critical target role skill gaps: {', '.join(missing_skills[:4])}.")
        if project_count < 2:
            weaknesses.append("Needs more end-to-end practical project experience.")
        if not weaknesses:
            weaknesses.append("Continue building advanced cloud-scale deployments.")

        # Determine Career Stage
        if total_score >= 80:
            career_stage = "Advanced / Placement-Ready Candidate"
        elif total_score >= 65:
            career_stage = "Intermediate / Approaching Role Readiness"
        elif total_score >= 45:
            career_stage = "Pre-Specialization Foundation"
        else:
            career_stage = "Early Career / Foundation Stage"

        display_name = profile.get_display_name()
        summary = (
            f"{display_name} is currently targeting {target_role}. "
            f"The profile matches {len(matched_skills)} required technical skills. "
            f"The AI-estimated readiness score is {total_score}%, reflecting required skill match ({required_skills_score}/40), "
            f"projects experience ({projects_experience_score}/25), education ({education_certs_score}/15), and role alignment ({role_gaps_score}/20)."
        )

        return ProfileAgentOutput(
            summary=summary,
            strengths=strengths,
            weaknesses=weaknesses,
            career_stage=career_stage,
            readiness_estimate=total_score,
            breakdown=breakdown
        )

profile_agent = ProfileAgent()
