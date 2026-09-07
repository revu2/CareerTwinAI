from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import ChatResponse
from .gap_analyzer_agent import gap_analyzer_agent
from .roadmap_agent import roadmap_agent
from .branding_agent import branding_agent
from .interview_agent import interview_agent
from .scout_agent import scout_agent

class TwinAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CareerTwin Core Orchestrator",
            role_description="the student's personal AI Career Digital Twin and holistic career strategy copilot."
        )

    def compute_composite_readiness(self, profile: StudentProfile) -> float:
        """Calculate composite 0-100 readiness index based on skills, projects, experiences, and education."""
        analysis = gap_analyzer_agent.analyze(profile)
        base_match = analysis.overall_match_percentage

        # Boosts & adjustments
        gpa_factor = (profile.education.gpa or 3.0) / 4.0 * 5.0
        project_count_factor = min(len(profile.projects) * 3, 10)
        cert_count_factor = min(len(profile.certifications) * 2.5, 5)
        exp_factor = min(len(profile.experiences) * 5, 10)

        composite = (base_match * 0.70) + gpa_factor + project_count_factor + cert_count_factor + exp_factor
        return round(min(max(composite, 40.0), 98.0), 1)

    def chat_with_twin(
        self,
        profile: StudentProfile,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> ChatResponse:
        target_role = profile.target_career.role_title
        student_skills = ", ".join(profile.skills.all_technical_skills())
        projects_summary = "; ".join([f"{p.title} ({', '.join(p.tech_stack)})" for p in profile.projects])
        certs_str = str([c.name for c in profile.certifications])
        exps_str = str([e.role + ' at ' + e.company for e in profile.experiences])

        history_context = ""
        if chat_history:
            history_context = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in chat_history[-6:]])

        prompt = f"""
You are CareerTwin AI — the personalized AI Career Digital Twin for {profile.name}.

Student Identity & Profile Context:
- Candidate Name: {profile.name}
- Degree & University: {profile.education.degree}, {profile.education.university} (Grad: {profile.education.graduation_year}, GPA: {profile.education.gpa})
- Target Career: {target_role} ({profile.target_career.target_tier})
- Timeline & Study: {profile.target_career.timeline_months} months target ({profile.target_career.weekly_study_hours} hrs/wk)
- Current Technical Skills: {student_skills}
- Projects: {projects_summary or 'None added yet'}
- Certifications: {certs_str}
- Experiences: {exps_str}
- Twin Readiness Index: {profile.readiness_score}%

Conversation History:
{history_context}

Student Message: "{user_message}"

Respond as their smart, encouraging, highly technical career twin. Be direct, actionable, and reference their specific background and target role.
Keep formatting clean with bullet points where helpful.
Also provide 2-3 quick suggested next actions.

Return strict JSON matching this schema:
{{
    "response": "Your markdown-formatted response message to the student",
    "suggested_actions": [
        {{"label": "Run Skill Gap Analysis", "action_code": "GAP_ANALYSIS"}},
        {{"label": "Generate Upskilling Roadmap", "action_code": "GENERATE_ROADMAP"}},
        {{"label": "Start Mock Interview", "action_code": "START_INTERVIEW"}}
    ]
}}
"""

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "response" in parsed:
            return ChatResponse(
                response=parsed.get("response", ""),
                agent_name="CareerTwin Core",
                suggested_actions=parsed.get("suggested_actions", [
                    {"label": "Analyze Skill Gaps", "action_code": "GAP_ANALYSIS"},
                    {"label": "View Roadmap", "action_code": "GENERATE_ROADMAP"},
                    {"label": "Practice Mock Interview", "action_code": "START_INTERVIEW"}
                ]),
                twin_state_summary={
                    "name": profile.name,
                    "target_role": target_role,
                    "readiness_score": profile.readiness_score,
                    "skills_count": len(profile.skills.all_technical_skills())
                }
            )

        # Fallback Heuristic Response
        return self._heuristic_chat(profile, user_message)

    def _heuristic_chat(self, profile: StudentProfile, message: str) -> ChatResponse:
        msg_lower = message.lower()
        target_role = profile.target_career.role_title
        name = profile.name

        if any(w in msg_lower for w in ["interview", "mock", "question", "prepare"]):
            reply = (
                f"Hey {name}! To prep for your upcoming **{target_role}** interviews, I recommend focusing on three pillars:\n\n"
                f"1. **Core Technical Fundamentals:** Drill down into {profile.skills.languages[0] if profile.skills.languages else 'Python/C++'} data structures and algorithms.\n"
                f"2. **System Design & Architecture:** Practice explaining component trade-offs for high-concurrency architectures.\n"
                f"3. **STAR Stories:** Be ready to talk in-depth about '{profile.projects[0].title if profile.projects else 'your projects'}' with quantifiable metric results.\n\n"
                f"Would you like to start a simulated mock interview round right now?"
            )
            actions = [
                {"label": "Start Mock Interview", "action_code": "START_INTERVIEW"},
                {"label": "Review Skill Gaps", "action_code": "GAP_ANALYSIS"}
            ]
        elif any(w in msg_lower for w in ["gap", "missing", "improve", "skill", "benchmark"]):
            reply = (
                f"Based on your current profile ({profile.education.degree} at {profile.education.university or 'your university'}), "
                f"your **Twin Readiness Score is {profile.readiness_score}%** for **{target_role}**.\n\n"
                f"- **Strengths:** Strong baseline in {', '.join(profile.skills.languages[:3]) or 'software engineering fundamentals'}.\n"
                f"- **High-Yield Gaps to Close:** Adding deeper production experience with containerization, cloud deployment, and scalable data layers.\n\n"
                f"I can generate a step-by-step milestone roadmap to bridge these gaps over your {profile.target_career.timeline_months}-month target timeline."
            )
            actions = [
                {"label": "Generate Upskilling Roadmap", "action_code": "GENERATE_ROADMAP"},
                {"label": "Optimize Resume for ATS", "action_code": "OPTIMIZE_RESUME"}
            ]
        elif any(w in msg_lower for w in ["resume", "cv", "ats", "bullet"]):
            reply = (
                f"Your resume currently features strong project work like '{profile.projects[0].title if profile.projects else 'your portfolio'}'.\n\n"
                f"To maximize recruiter callbacks for **{target_role}**, we should apply the **Google XYZ Impact Formula**:\n"
                f"*'Accomplished [X], as measured by [Y], by doing [Z]'*.\n\n"
                f"Head over to our **Resume Studio** to see automated bullet point transformations and check your ATS keyword score."
            )
            actions = [
                {"label": "Open Resume Studio", "action_code": "OPTIMIZE_RESUME"},
                {"label": "Match a Job Description", "action_code": "SCOUT_JOB"}
            ]
        else:
            reply = (
                f"Hello {name}! I am your **CareerTwin AI Copilot**.\n\n"
                f"I have synchronized your academic background at **{profile.education.university or 'University'}**, "
                f"your skills ({', '.join(profile.skills.all_technical_skills()[:4]) or 'technical stack'}), and your target goal of becoming a **{target_role}**.\n\n"
                f"Here is what we can do together:\n"
                f"- **Skill Gap Analysis:** Benchmark your profile against industry standards.\n"
                f"- **Personalized Roadmap:** Step-by-step upskilling plan tailored to your {profile.target_career.weekly_study_hours} hrs/week schedule.\n"
                f"- **ATS Resume Studio:** Polish bullet points with metrics and keywords.\n"
                f"- **AI Mock Interviews:** Practice with real-time technical scoring and feedback.\n"
                f"- **Opportunity Scout:** Tailor cover letters and pitch emails for target openings."
            )
            actions = [
                {"label": "Run Skill Gap Analysis", "action_code": "GAP_ANALYSIS"},
                {"label": "Generate Roadmap", "action_code": "GENERATE_ROADMAP"},
                {"label": "Practice Mock Interview", "action_code": "START_INTERVIEW"}
            ]

        return ChatResponse(
            response=reply,
            agent_name="CareerTwin Core",
            suggested_actions=actions,
            twin_state_summary={
                "name": profile.name,
                "target_role": target_role,
                "readiness_score": profile.readiness_score,
                "skills_count": len(profile.skills.all_technical_skills())
            }
        )

twin_agent = TwinAgent()
