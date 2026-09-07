from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import (
    CareerStrategistAgentOutput,
    ProfileAgentOutput,
    SkillGapAgentOutput,
    CareerRoadmapAgentOutput,
    ProjectAgentOutput,
    SimulationAgentOutput
)

class CareerStrategistAgent(BaseAgent):
    """
    AGENT 5: CAREER STRATEGIST AGENT
    Responsibilities:
    - Act as the final strategic advisor
    - Receive synthesized outputs from all other agents
    - Combine findings into a unified personalized strategic master plan
    """
    def __init__(self):
        super().__init__(
            name="Career Strategist Agent",
            role_description="an executive career coach and chief career strategist synthesizing all agent intelligence."
        )

    def formulate_strategy(
        self,
        profile: StudentProfile,
        profile_out: ProfileAgentOutput,
        gap_out: SkillGapAgentOutput,
        roadmap_out: CareerRoadmapAgentOutput,
        project_out: ProjectAgentOutput,
        simulation_out: SimulationAgentOutput
    ) -> CareerStrategistAgentOutput:
        target = profile.target_career
        display_name = profile.name.strip() if profile.name and profile.name.strip() else "The student"
        missing_str = ", ".join(gap_out.missing_skills[:4])
        projects_rec_str = ", ".join([p.title for p in project_out.recommended_projects])

        prompt = f"""
        Formulate a comprehensive, final strategic career action plan for a student.

        Candidate: {display_name} ({profile.degree} in {profile.branch}, Year: {profile.year_of_study}, CGPA: {profile.cgpa})
        Target Career Role: {target}
        Current Readiness Score: {profile_out.readiness_estimate}%
        Current Strengths Identified: {', '.join(profile_out.strengths)}
        Key Missing Skill Gaps: {missing_str}
        Recommended Flagship Projects: {projects_rec_str}
        Projected Readiness with Upskilling: {simulation_out.future_simulated_twin.readiness_score}%

        Synthesize all findings and provide:
        1. Current Career Assessment (2-3 paragraphs)
        2. Top Strengths (3 key bullet points)
        3. Biggest Gaps (3 key bullet points)
        4. Immediate Next Steps (Next 14 Days)
        5. Short-Term Strategy (Months 1-3)
        6. Long-Term Strategy (Months 4-6 & Placement Season)
        7. Action Priority Matrix (High Impact / Low Effort vs High Impact / High Effort)

        Return strict JSON matching this schema:
        {{
            "current_career_assessment": "Comprehensive assessment text referencing candidate dynamically",
            "top_strengths": ["Strength 1", "Strength 2", "Strength 3"],
            "biggest_gaps": ["Gap 1", "Gap 2", "Gap 3"],
            "immediate_next_steps": ["Step 1", "Step 2", "Step 3"],
            "short_term_strategy": ["Strategy item 1", "Strategy item 2"],
            "long_term_strategy": ["Long term item 1", "Long term item 2"],
            "action_priority_matrix": {{
                "Immediate High-Yield (Weeks 1-2)": "Action 1",
                "Deep Core Build (Months 1-3)": "Action 2",
                "Capstone & Outreach (Months 4-6)": "Action 3"
            }}
        }}
        """

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "immediate_next_steps" in parsed and "current_career_assessment" in parsed:
            return CareerStrategistAgentOutput(
                current_career_assessment=parsed.get("current_career_assessment", ""),
                top_strengths=parsed.get("top_strengths", []),
                biggest_gaps=parsed.get("biggest_gaps", []),
                immediate_next_steps=parsed.get("immediate_next_steps", []),
                short_term_strategy=parsed.get("short_term_strategy", []),
                long_term_strategy=parsed.get("long_term_strategy", []),
                action_priority_matrix=parsed.get("action_priority_matrix", {})
            )

        # Fallback Heuristic Master Strategy
        return self._heuristic_strategy(profile, profile_out, gap_out, roadmap_out, project_out, simulation_out)

    def _heuristic_strategy(
        self,
        profile: StudentProfile,
        profile_out: ProfileAgentOutput,
        gap_out: SkillGapAgentOutput,
        roadmap_out: CareerRoadmapAgentOutput,
        project_out: ProjectAgentOutput,
        simulation_out: SimulationAgentOutput
    ) -> CareerStrategistAgentOutput:
        target = profile.target_career
        name_ref = profile.name.strip() if profile.name and profile.name.strip() else "The student"
        pronoun_pos = f"{profile.name}'s" if profile.name and profile.name.strip() else "the candidate's"
        top_missing = gap_out.missing_skills[0] if gap_out.missing_skills else "PyTorch & Deep Learning"
        second_missing = gap_out.missing_skills[1] if len(gap_out.missing_skills) > 1 else "FastAPI & Docker"

        assessment = (
            f"{name_ref} is positioned at an exciting inflection point. With a solid academic foundation in {profile.branch} "
            f"and hands-on familiarity in Python and SQL, the foundational building blocks are in place. However, current market "
            f"competitiveness for {target} roles requires transitioning from basic scripting to building and deploying production-grade "
            f"deep learning systems. By adhering to the 5-phase roadmap and completing the recommended flagship projects, "
            f"{pronoun_pos} digital twin readiness index is projected to climb from {profile_out.readiness_estimate}% to "
            f"{simulation_out.future_simulated_twin.readiness_score}%, opening doors to top-tier internship and full-time hiring pipelines."
        )

        immediate_steps = [
            f"Complete a 10-hour deep dive on {top_missing} fundamentals, writing code in PyTorch/Python daily.",
            f"Set up GitHub repository structure for the flagship project '{project_out.recommended_projects[0].title}'.",
            "Commit to a structured schedule: 2 hours of hands-on coding + 1 hour of algorithmic problem solving 5 days a week."
        ]

        short_term = [
            f"Phase 2 & 3 Execution: Implement core model training and integrate {second_missing} for asynchronous API inference.",
            "Containerize all development environments with Docker to guarantee reproducible builds on GitHub.",
            "Write weekly technical documentation and architectural write-ups on LinkedIn / personal portfolio."
        ]

        long_term = [
            "Deploy live cloud demos with custom domain names and comprehensive GitHub README benchmarks.",
            "Conduct 10+ mock interview simulations focusing on AI system design trade-offs and STAR behavioral questions.",
            "Initiate targeted cold outreach to engineering hiring managers at dream companies with personalized project walk-throughs."
        ]

        matrix = {
            "Immediate Quick Wins (Weeks 1-2)": f"Master {top_missing} syntax + Initialize public GitHub repo",
            "High-Impact Engineering (Months 1-3)": f"Build '{project_out.recommended_projects[0].title}' + Dockerize backend",
            "Placement & Interview Dominance (Months 4-6)": "System design whiteboarding + ATS resume alignment"
        }

        return CareerStrategistAgentOutput(
            current_career_assessment=assessment,
            top_strengths=profile_out.strengths[:3] or ["Python and SQL fundamentals", "Strong academic coursework"],
            biggest_gaps=gap_out.missing_skills[:3] or ["Deep Learning Frameworks", "Production Deployment", "RAG Architecture"],
            immediate_next_steps=immediate_steps,
            short_term_strategy=short_term,
            long_term_strategy=long_term,
            action_priority_matrix=matrix
        )

strategist_agent = CareerStrategistAgent()
