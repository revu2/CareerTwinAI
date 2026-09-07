from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import OpportunityMatchResult

class ScoutAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Opportunity Scout & Application Matcher Agent",
            role_description="an executive talent scout and outbound career strategist."
        )

    def match_opportunity(
        self,
        profile: StudentProfile,
        job_title: str,
        company: str,
        job_description: str
    ) -> OpportunityMatchResult:
        student_skills = profile.skills.all_technical_skills()
        projs_str = str([p.title + ': ' + p.description for p in profile.projects])
        exps_str = str([e.role + ' at ' + e.company for e in profile.experiences])

        prompt = f"""
Analyze candidate fit for the following job opportunity and craft application assets.

Candidate:
- Name: {profile.name}
- University: {profile.education.university} ({profile.education.degree}, GPA {profile.education.gpa})
- Skills: {', '.join(student_skills)}
- Projects: {projs_str}
- Experiences: {exps_str}

Job Opportunity:
- Role Title: {job_title}
- Company: {company}
- Description: {job_description}

1. Calculate match percentage (0-100).
2. List matched skills and missing skills.
3. Write a concise Twin Fit Summary.
4. Write a tailored, persuasive 3-paragraph Cover Letter.
5. Write a high-converting 100-word Cold Outreach Email / LinkedIn InMail to the hiring manager.
6. Provide 3 Key Interview Talking Points connecting candidate's projects to this job.

Return strict JSON matching this schema:
{{
    "match_percentage": 85.0,
    "matched_skills": ["Skill1", "Skill2"],
    "missing_skills": ["Skill3", "Skill4"],
    "twin_fit_summary": "Summary of why the candidate is a strong fit",
    "tailored_cover_letter": "Full text of cover letter",
    "cold_outreach_email": "Subject: ... \\n\\nBody: ...",
    "key_interview_talking_points": [
        "Point 1", "Point 2", "Point 3"
    ]
}}
"""

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "match_percentage" in parsed and "tailored_cover_letter" in parsed:
            return OpportunityMatchResult(
                job_title=job_title,
                company=company,
                match_percentage=float(parsed.get("match_percentage", 78)),
                matched_skills=parsed.get("matched_skills", []),
                missing_skills=parsed.get("missing_skills", []),
                twin_fit_summary=parsed.get("twin_fit_summary", f"Strong match for {job_title} at {company}."),
                tailored_cover_letter=parsed.get("tailored_cover_letter", ""),
                cold_outreach_email=parsed.get("cold_outreach_email", ""),
                key_interview_talking_points=parsed.get("key_interview_talking_points", [])
            )

        # Fallback Heuristic Matcher
        return self._heuristic_match(profile, job_title, company, job_description)

    def _heuristic_match(
        self,
        profile: StudentProfile,
        job_title: str,
        company: str,
        job_desc: str
    ) -> OpportunityMatchResult:
        desc_lower = job_desc.lower()
        student_skills = profile.skills.all_technical_skills()
        
        matched = []
        missing = []
        for s in student_skills:
            if s.lower() in desc_lower:
                matched.append(s)

        # Check some common requirements
        common_reqs = ["Docker", "Kubernetes", "AWS", "CI/CD", "Redis", "FastAPI", "React", "PostgreSQL", "System Design"]
        for req in common_reqs:
            if req.lower() in desc_lower and req.lower() not in [s.lower() for s in student_skills]:
                missing.append(req)

        match_score = min(max(int((len(matched) / max(len(matched) + len(missing), 1)) * 100), 55), 94)

        fit_summary = (
            f"{profile.name} demonstrates a {match_score}% competency match for the {job_title} role at {company}. "
            f"Strong alignment across {', '.join(matched[:3]) or 'core software engineering foundations'}."
        )

        project_mention = profile.projects[0].title if profile.projects else "recent distributed systems work"

        cover_letter = (
            f"Dear Hiring Team at {company},\n\n"
            f"I am writing to express my enthusiastic interest in the {job_title} position. As a Computer Science student at {profile.education.university or 'University'} "
            f"specializing in {profile.target_career.role_title}, I have developed deep technical expertise in {', '.join(student_skills[:4])}.\n\n"
            f"Recently, I architected '{project_mention}', where I focused on scalable system architecture, high-performance data processing, and production reliability. "
            f"I have consistently sought out engineering challenges that bridge rigorous computer science principles with high-impact software delivery.\n\n"
            f"I am particularly inspired by {company}'s innovative work, and I am eager to bring my proactive problem-solving, rapid adaptability, and technical drive to your team. "
            f"Thank you for your time and consideration, and I welcome the opportunity to discuss how my skill set aligns with your engineering goals.\n\n"
            f"Sincerely,\n{profile.name}\n{profile.email}"
        )

        outreach = (
            f"Subject: {profile.name} — {profile.education.degree} ({profile.education.graduation_year}) / {job_title} Interest\n\n"
            f"Hi {company} Engineering Team,\n\n"
            f"I came across the {job_title} role at {company} and was immediately drawn to your engineering culture and product trajectory.\n\n"
            f"As a CS student at {profile.education.university or 'University'} with hands-on experience in {', '.join(student_skills[:3])}, I recently built '{project_mention}'. "
            f"I'd love the opportunity to share how my background in scalable architectures could contribute to your current sprint priorities.\n\n"
            f"Would you be open to a brief 10-minute chat sometime next week?\n\n"
            f"Best regards,\n{profile.name}\n{profile.portfolio_url or profile.github_url or profile.email}"
        )

        talking_points = [
            f"Highlight your engineering decisions in '{project_mention}' and connect them to {company}'s scale challenges.",
            f"Emphasize your proficiency in {matched[0] if matched else 'core programming'} and rapid ramp-up cycle on modern frameworks.",
            f"Discuss your approach to system reliability, testing, and continuous deployment."
        ]

        return OpportunityMatchResult(
            job_title=job_title,
            company=company,
            match_percentage=float(match_score),
            matched_skills=matched or student_skills[:4],
            missing_skills=missing[:4],
            twin_fit_summary=fit_summary,
            tailored_cover_letter=cover_letter,
            cold_outreach_email=outreach,
            key_interview_talking_points=talking_points
        )

scout_agent = ScoutAgent()
