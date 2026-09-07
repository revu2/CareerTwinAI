from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import SkillGapAnalysisResult
from ..data.role_benchmarks import get_role_benchmark

class GapAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Skill Gap & Market Intelligence Agent",
            role_description="an expert technical recruiter and industry skill benchmark specialist."
        )

    def analyze(self, profile: StudentProfile) -> SkillGapAnalysisResult:
        target_role = profile.target_career.role_title
        benchmark = get_role_benchmark(target_role)

        # First, attempt to run via LLM for hyper-personalized analysis if client is active
        student_skills = profile.skills.all_technical_skills()
        core_skills_str = ", ".join(benchmark.get("core_skills", []))
        important_skills_str = ", ".join(benchmark.get("important_skills", []))
        proj_str = str([p.title + ': ' + ', '.join(p.tech_stack) for p in profile.projects])
        cert_str = str([c.name for c in profile.certifications])
        exp_str = str([e.role + ' at ' + e.company for e in profile.experiences])

        prompt = f"""
Analyze this student's skill profile against the target career role: '{target_role}'.

Student Name: {profile.name}
Degree: {profile.education.degree} ({profile.education.university})
Graduation Year: {profile.education.graduation_year}, GPA: {profile.education.gpa}
Technical Skills: {', '.join(student_skills)}
Projects: {proj_str}
Certifications: {cert_str}
Experiences: {exp_str}

Industry Benchmark Core Skills: {core_skills_str}
Important Skills: {important_skills_str}

Return a strictly valid JSON object matching this schema:
{{
    "overall_match_percentage": 75.0,
    "readiness_grade": "B+",
    "summary_verdict": "Concise evaluation of current readiness",
    "strengths": [
        {{"skill": "Skill Name", "student_level": "Proficient", "reason": "Why this is an asset"}}
    ],
    "critical_gaps": [
        {{"skill": "Missing Skill", "importance": "High", "target_level": "Intermediate", "recommended_action": "What to learn/build"}}
    ],
    "secondary_gaps": [
        {{"skill": "Secondary Tool/Skill", "importance": "Medium", "target_level": "Familiar", "recommended_action": "Quick study guide"}}
    ],
    "radar_chart": {{
        "categories": ["Languages", "Frameworks & Architecture", "Databases & Storage", "DevOps & Cloud", "Projects & Experience", "CS Fundamentals"],
        "student_scores": [75, 80, 70, 65, 80, 85],
        "benchmark_scores": [90, 85, 80, 75, 85, 80]
    }},
    "key_recommendations": [
        "Actionable tip 1", "Actionable tip 2", "Actionable tip 3"
    ]
}}
"""

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "overall_match_percentage" in parsed and "radar_chart" in parsed:
            return SkillGapAnalysisResult(
                target_role=target_role,
                overall_match_percentage=float(parsed.get("overall_match_percentage", 70)),
                readiness_grade=str(parsed.get("readiness_grade", "B")),
                summary_verdict=str(parsed.get("summary_verdict", f"Solid foundation for {target_role} with key areas to upgrade.")),
                strengths=parsed.get("strengths", []),
                critical_gaps=parsed.get("critical_gaps", []),
                secondary_gaps=parsed.get("secondary_gaps", []),
                radar_chart=parsed.get("radar_chart", {}),
                key_recommendations=parsed.get("key_recommendations", [])
            )

        # Deterministic Heuristic Engine Fallback
        return self._heuristic_analysis(profile, benchmark)

    def _heuristic_analysis(self, profile: StudentProfile, benchmark: Dict[str, Any]) -> SkillGapAnalysisResult:
        target_role = profile.target_career.role_title
        student_skills_all = [s.lower() for s in profile.skills.all_technical_skills()]
        
        # Add tech stack from projects
        for p in profile.projects:
            for t in p.tech_stack:
                student_skills_all.append(t.lower())
        student_skills_set = set(student_skills_all)

        core_skills = benchmark.get("core_skills", [])
        important_skills = benchmark.get("important_skills", [])

        matched_core = [s for s in core_skills if s.lower() in student_skills_set]
        missing_core = [s for s in core_skills if s.lower() not in student_skills_set]
        matched_important = [s for s in important_skills if s.lower() in student_skills_set]
        missing_important = [s for s in important_skills if s.lower() not in student_skills_set]

        # Calculate score
        core_ratio = len(matched_core) / max(len(core_skills), 1)
        important_ratio = len(matched_important) / max(len(important_skills), 1)
        project_boost = min(len(profile.projects) * 5, 15)
        exp_boost = min(len(profile.experiences) * 10, 20)

        raw_score = (core_ratio * 55) + (important_ratio * 25) + project_boost + exp_boost
        overall_match = round(min(max(raw_score, 35.0), 96.0), 1)

        # Grade
        if overall_match >= 90:
            grade = "A+"
        elif overall_match >= 85:
            grade = "A"
        elif overall_match >= 75:
            grade = "B+"
        elif overall_match >= 65:
            grade = "B"
        elif overall_match >= 55:
            grade = "C+"
        else:
            grade = "C"

        strengths = []
        for skill in matched_core[:5]:
            strengths.append({
                "skill": skill,
                "student_level": "Competent / Applied",
                "reason": f"Directly satisfies core industry requirement for {target_role} positions."
            })
        for skill in matched_important[:3]:
            strengths.append({
                "skill": skill,
                "student_level": "Familiar",
                "reason": f"Valuable differentiator in technical interviews for {target_role}."
            })

        critical_gaps = []
        for skill in missing_core[:4]:
            critical_gaps.append({
                "skill": skill,
                "importance": "High",
                "target_level": "Intermediate / Project-ready",
                "recommended_action": f"Build a hands-on project incorporating {skill} and demonstrate production patterns."
            })

        secondary_gaps = []
        for skill in missing_important[:4]:
            secondary_gaps.append({
                "skill": skill,
                "importance": "Medium",
                "target_level": "Working Knowledge",
                "recommended_action": f"Review official documentation and complete a starter tutorial on {skill}."
            })

        # Calculate radar chart scores
        benchmark_radar = benchmark.get("radar_categories", {
            "Core Programming": 85,
            "Frameworks & Architecture": 80,
            "Databases & Storage": 75,
            "DevOps & Infrastructure": 70,
            "Projects & System Design": 75,
            "CS Fundamentals": 80
        })

        categories = list(benchmark_radar.keys())
        bench_values = list(benchmark_radar.values())
        student_values = []
        
        for i, val in enumerate(bench_values):
            factor = (overall_match / 100.0) * (0.85 + (i % 3) * 0.1)
            score = round(min(val * factor, 98.0))
            student_values.append(max(score, 30))

        radar_data = {
            "categories": categories,
            "student_scores": student_values,
            "benchmark_scores": bench_values
        }

        key_recs = [
            f"Prioritize mastering {missing_core[0] if missing_core else 'advanced system patterns'} through an end-to-end portfolio project.",
            f"Refactor resume bullet points to highlight measurable outcomes with {matched_core[0] if matched_core else 'your primary stack'}.",
            f"Practice system design interviews focusing on scaling and database optimization."
        ]

        summary_verdict = (
            f"Candidate demonstrates {overall_match}% alignment with standard {target_role} expectations. "
            f"Core strengths in {', '.join(matched_core[:3]) or 'foundational programming'} provide strong momentum, "
            f"while addressing {missing_core[0] if missing_core else 'advanced tooling'} will elevate profile to interview readiness."
        )

        return SkillGapAnalysisResult(
            target_role=target_role,
            overall_match_percentage=overall_match,
            readiness_grade=grade,
            summary_verdict=summary_verdict,
            strengths=strengths,
            critical_gaps=critical_gaps,
            secondary_gaps=secondary_gaps,
            radar_chart=radar_data,
            key_recommendations=key_recs
        )

gap_analyzer_agent = GapAnalyzerAgent()
