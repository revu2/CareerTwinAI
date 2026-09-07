from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import SkillGapAgentOutput
from ..data.role_benchmarks import get_role_benchmark
from ..services.resume_parser import extract_skills_from_text

class SkillGapAgent(BaseAgent):
    """
    AGENT 2: SKILL GAP AGENT
    Responsibilities:
    - Compare student's current skills with target career role benchmarks and custom JD
    - Categorize skills into: 1. Strong, 2. Developing, 3. Missing
    - Identify priority skills to learn first
    """
    def __init__(self):
        super().__init__(
            name="Skill Gap Agent",
            role_description="an industry skill benchmark specialist that detects competency gaps for target roles."
        )

    def analyze_gaps(self, profile: StudentProfile) -> SkillGapAgentOutput:
        target_role = profile.target_career or "AI Engineer"
        benchmark = get_role_benchmark(target_role)
        current_skills = profile.get_skills_list()
        
        core_skills = list(benchmark.get("core_skills", []))
        important_skills = list(benchmark.get("important_skills", []))

        # Merge skills from custom Job Description if provided
        if profile.job_description and profile.job_description.strip():
            jd_skills = extract_skills_from_text(profile.job_description)
            for jds in jd_skills:
                if jds not in core_skills and jds not in important_skills:
                    core_skills.append(jds)

        required_skills = core_skills + important_skills[:4]

        prompt = f"""
        Compare this student's skills against the industry standard requirements for the role: '{target_role}'.

        Student Skills: {', '.join(current_skills)}
        Role Required Core Skills: {', '.join(core_skills)}
        Role Important Skills: {', '.join(important_skills)}

        Categorize skills into:
        1. Strong: Skills student possesses that directly match the role
        2. Developing: Skills student has started or has basic familiarity with
        3. Missing: Vital industry skills completely absent from student profile
        4. Priority Skills: Top 3-4 skills the student MUST learn first to become competitive.

        Return strictly valid JSON matching this schema:
        {{
            "target_role": "{target_role}",
            "overall_match_percentage": 52.0,
            "required_skills": {str(required_skills)},
            "current_skills": {str(current_skills)},
            "strong_skills": ["Strong skill 1", "Strong skill 2"],
            "developing_skills": ["Developing skill 1"],
            "missing_skills": ["Missing skill 1", "Missing skill 2", "Missing skill 3"],
            "priority_skills": ["Priority skill 1", "Priority skill 2"],
            "radar_data": {{
                "categories": ["Languages", "Frameworks", "Databases", "Cloud & Deployment", "System Design", "CS Fundamentals"],
                "student_scores": [75, 40, 65, 30, 45, 70],
                "benchmark_scores": [90, 85, 80, 75, 80, 85]
            }}
        }}
        """

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "missing_skills" in parsed and "priority_skills" in parsed:
            return SkillGapAgentOutput(
                target_role=target_role,
                overall_match_percentage=float(parsed.get("overall_match_percentage", 48.0)),
                required_skills=parsed.get("required_skills", required_skills),
                current_skills=parsed.get("current_skills", current_skills),
                strong_skills=parsed.get("strong_skills", []),
                developing_skills=parsed.get("developing_skills", []),
                missing_skills=parsed.get("missing_skills", []),
                priority_skills=parsed.get("priority_skills", []),
                radar_data=parsed.get("radar_data", {})
            )

        # Deterministic Heuristic Analysis
        return self._heuristic_analysis(profile, benchmark, core_skills, important_skills)

    def _heuristic_analysis(self, profile: StudentProfile, benchmark: Dict[str, Any], core_skills: List[str], important_skills: List[str]) -> SkillGapAgentOutput:
        target_role = profile.target_career or "AI Engineer"
        student_skills = profile.get_skills_list()
        student_skills_lower = [s.strip().lower() for s in student_skills if s.strip()]

        def is_matched(req: str) -> bool:
            r = req.lower().strip()
            for s in student_skills_lower:
                if s == r or s in r or r in s:
                    return True
            return False

        strong = []
        developing = []
        missing = []

        for skill in core_skills:
            if is_matched(skill):
                strong.append(skill)
            else:
                missing.append(skill)

        for skill in important_skills:
            if is_matched(skill):
                developing.append(skill)
            else:
                if skill not in missing:
                    missing.append(skill)

        # Priority skills are the first 3 critical missing skills
        priority = missing[:3] if missing else ["System Design & Architecture", "Performance Optimization"]

        # Calculate match percentage
        total_req = len(core_skills) + len(important_skills)
        matched_count = len(strong) + (len(developing) * 0.5)
        raw_match = (matched_count / max(total_req, 1)) * 100
        match_percentage = round(min(max(raw_match, 25.0), 98.0), 1)

        # Dynamic Radar Chart based on role benchmarks
        radar_cats = benchmark.get("radar_categories", {
            "Languages": 90,
            "Frameworks": 85,
            "Databases": 80,
            "DevOps & Cloud": 75,
            "System Design": 80,
            "CS Fundamentals": 85
        })

        bench_categories = list(radar_cats.keys())
        bench_scores = list(radar_cats.values())

        # Calculate student scores for each dimension
        student_scores = []
        for cat in bench_categories:
            cat_l = cat.lower()
            if any(k in cat_l for k in ["lang", "python", "java", "c++", "script"]):
                s_score = 80 if any(k in student_skills_lower for k in ["python", "java", "javascript", "typescript", "c++", "c"]) else 40
            elif any(k in cat_l for k in ["frame", "ml", "react", "spring", "fastapi", "torch"]):
                s_score = 75 if any(k in student_skills_lower for k in ["react", "pytorch", "tensorflow", "fastapi", "spring boot", "django", "node.js"]) else 35
            elif any(k in cat_l for k in ["data", "sql", "db", "storage"]):
                s_score = 80 if any(k in student_skills_lower for k in ["sql", "postgresql", "mysql", "mongodb", "redis"]) else 40
            elif any(k in cat_l for k in ["cloud", "devops", "docker", "k8s", "ci"]):
                s_score = 70 if any(k in student_skills_lower for k in ["docker", "kubernetes", "aws", "gcp", "azure", "git", "ci/cd"]) else 30
            elif any(k in cat_l for k in ["design", "arch", "system"]):
                s_score = 65 if len(profile.projects) >= 2 else 40
            else:
                s_score = 80 if (profile.cgpa and profile.cgpa >= 8.0) else 65
            student_scores.append(s_score)

        radar_data = {
            "categories": bench_categories,
            "student_scores": student_scores,
            "benchmark_scores": bench_scores
        }

        return SkillGapAgentOutput(
            target_role=target_role,
            overall_match_percentage=match_percentage,
            required_skills=core_skills + important_skills[:3],
            current_skills=profile.get_skills_list(),
            strong_skills=strong,
            developing_skills=developing,
            missing_skills=missing,
            priority_skills=priority,
            radar_data=radar_data
        )

skill_gap_agent = SkillGapAgent()
