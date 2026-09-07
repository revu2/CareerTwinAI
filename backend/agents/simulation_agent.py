from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import (
    SimulationAgentOutput,
    TwinStateSnapshot,
    SkillGapAgentOutput
)

class FutureCareerSimulationAgent(BaseAgent):
    """
    AGENT 6: FUTURE CAREER SIMULATION AGENT (FLAGSHIP UNIQUE FEATURE)
    Responsibilities:
    - Accepts hypothetical "What-If" student actions
    - Simulates career trajectory, readiness score jump, and gap closures
    - Provides a clear side-by-side comparison: CURRENT TWIN vs FUTURE SIMULATED TWIN
    """
    def __init__(self):
        super().__init__(
            name="Future Career Simulation Agent",
            role_description="an AI trajectory simulator that projects how hypothetical upskilling decisions transform career readiness."
        )

    def simulate_future(
        self,
        profile: StudentProfile,
        gap_output: SkillGapAgentOutput,
        selected_actions: List[str],
        custom_scenario: Optional[str] = ""
    ) -> SimulationAgentOutput:
        current_score = profile.readiness_score
        target_role = profile.target_career
        display_name = profile.name.strip() if profile.name and profile.name.strip() else "The candidate"

        prompt = f"""
        Simulate the hypothetical career transformation for a student targeting: '{target_role}'.

        Current Digital Twin:
        - Candidate Name: {display_name}
        - Current Skills: {', '.join(profile.get_skills_list())}
        - Current Readiness Score: {current_score}/100
        - Missing Gaps: {', '.join(gap_output.missing_skills[:5])}

        What-If Hypothetical Actions Selected by Student:
        {selected_actions}
        Custom User Scenario: "{custom_scenario or 'Standard upskilling trajectory'}"

        Simulate the transformed FUTURE DIGITAL TWIN:
        1. Calculate realistic new readiness score (e.g. from {current_score} to 80-92/100).
        2. Identify which skill gaps are closed.
        3. List new technical capabilities unlocked.
        4. Provide side-by-side snapshot data for Current vs Future Twin.
        5. Write a concise simulation verdict referencing {display_name}.

        Return strict JSON matching this schema:
        {{
            "score_improvement": 38.0,
            "simulated_future_score": 86.0,
            "gaps_closed": ["PyTorch Deep Learning", "FastAPI Model Serving", "Docker"],
            "new_capabilities_unlocked": [
                "Deploying containerized transformer inference pipelines",
                "Architecting scalable vector search databases",
                "Confident system design whiteboarding"
            ],
            "current_twin_snapshot": {{
                "title": "Current Digital Twin",
                "readiness_score": {current_score},
                "skills_summary": {str(profile.get_skills_list())},
                "projects_count": {len(profile.projects)},
                "strengths_highlight": "Strong Python & CS coursework baseline",
                "unresolved_gaps": {str(gap_output.missing_skills[:3])},
                "competitive_tier": "Early Foundation / Pre-Specialization"
            }},
            "future_twin_snapshot": {{
                "title": "Simulated Future Twin",
                "readiness_score": 86.0,
                "skills_summary": ["Python", "PyTorch", "FastAPI", "Docker", "SQL", "Transformers", "RAG"],
                "projects_count": {len(profile.projects) + 2},
                "strengths_highlight": "End-to-End Deep Learning & Production Deployment",
                "unresolved_gaps": ["Advanced Distributed GPU Training (Senior-tier only)"],
                "competitive_tier": "Highly Competitive Tier-1 Ready"
            }},
            "simulation_verdict": "Clear summary of career trajectory shift"
        }}
        """

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "future_twin_snapshot" in parsed and "gaps_closed" in parsed:
            cur = parsed.get("current_twin_snapshot", {})
            fut = parsed.get("future_twin_snapshot", {})
            return SimulationAgentOutput(
                selected_actions=selected_actions,
                custom_scenario=custom_scenario,
                current_twin=TwinStateSnapshot(
                    title=cur.get("title", "Current Digital Twin"),
                    readiness_score=float(cur.get("readiness_score", current_score)),
                    skills_summary=cur.get("skills_summary", profile.get_skills_list()),
                    projects_count=int(cur.get("projects_count", len(profile.projects))),
                    strengths_highlight=cur.get("strengths_highlight", "Foundational Python skills"),
                    unresolved_gaps=cur.get("unresolved_gaps", gap_output.missing_skills[:3]),
                    competitive_tier=cur.get("competitive_tier", "Pre-Specialization")
                ),
                future_simulated_twin=TwinStateSnapshot(
                    title=fut.get("title", "Simulated Future Twin"),
                    readiness_score=float(fut.get("readiness_score", 86.0)),
                    skills_summary=fut.get("skills_summary", profile.get_skills_list() + ["PyTorch", "Docker"]),
                    projects_count=int(fut.get("projects_count", len(profile.projects) + 2)),
                    strengths_highlight=fut.get("strengths_highlight", "Fullstack AI System Architecture"),
                    unresolved_gaps=fut.get("unresolved_gaps", []),
                    competitive_tier=fut.get("competitive_tier", "Competitive Entry-Level AI Engineer")
                ),
                score_improvement=float(parsed.get("score_improvement", 38.0)),
                gaps_closed=parsed.get("gaps_closed", []),
                new_capabilities_unlocked=parsed.get("new_capabilities_unlocked", []),
                simulation_verdict=parsed.get("simulation_verdict", f"Hypothetical actions elevate profile into high-probability {target_role} interview pools.")
            )

        # Fallback Deterministic Trajectory Simulator
        return self._heuristic_simulation(profile, gap_output, selected_actions, custom_scenario)

    def _heuristic_simulation(
        self,
        profile: StudentProfile,
        gap_output: SkillGapAgentOutput,
        selected_actions: List[str],
        custom_scenario: Optional[str]
    ) -> SimulationAgentOutput:
        current_score = profile.readiness_score
        name_ref = profile.name.strip() if profile.name and profile.name.strip() else "the student"
        
        # Calculate impact boost based on actions
        action_boost = len(selected_actions) * 9.5
        if custom_scenario and len(custom_scenario.strip()) > 5:
            action_boost += 8.0

        simulated_score = round(min(current_score + max(action_boost, 28.0), 92.0), 1)
        score_diff = round(simulated_score - current_score, 1)

        gaps_to_close = gap_output.missing_skills[:len(selected_actions) + 1] or ["PyTorch Deep Learning", "FastAPI Serving", "Docker"]
        
        future_skills = list(dict.fromkeys(profile.get_skills_list() + ["PyTorch", "FastAPI", "Docker", "Hugging Face Transformers", "ChromaDB"]))

        current_snapshot = TwinStateSnapshot(
            title="Current Digital Twin",
            readiness_score=current_score,
            skills_summary=profile.get_skills_list(),
            projects_count=len(profile.projects),
            strengths_highlight="Strong CS coursework and foundational Python/SQL literacy",
            unresolved_gaps=gap_output.missing_skills[:3] or ["PyTorch", "Docker"],
            competitive_tier="Early Foundation / Pre-Specialization"
        )

        future_snapshot = TwinStateSnapshot(
            title="Simulated Future Twin",
            readiness_score=simulated_score,
            skills_summary=future_skills,
            projects_count=len(profile.projects) + 2,
            strengths_highlight="End-to-End Deep Learning Architecture & Production Model Serving",
            unresolved_gaps=["Advanced Distributed Multi-GPU Training (Senior-level requirement only)"],
            competitive_tier="Competitive Entry-Level / High-Match Candidate"
        )

        unlocked = [
            "Building and tuning neural networks in PyTorch from scratch",
            "Deploying scalable Retrieval-Augmented Generation (RAG) knowledge systems",
            "Packaging AI microservices in multi-stage Docker containers",
            "Confidently articulating architectural trade-offs during technical interviews"
        ]

        verdict = (
            f"If {name_ref} executes the selected upskilling initiatives, their Digital Twin Readiness Index "
            f"increases from {current_score}% to {simulated_score}% (+{score_diff}% gain). This hypothetical trajectory "
            f"bridges the critical {', '.join(gaps_to_close[:2])} gaps, transforming the profile from academic baseline "
            f"into a competitive candidate for {profile.target_career} opportunities."
        )

        return SimulationAgentOutput(
            selected_actions=selected_actions or ["Master PyTorch & Deep Learning", "Build 2 Production AI Projects", "Deploy with Docker"],
            custom_scenario=custom_scenario,
            current_twin=current_snapshot,
            future_simulated_twin=future_snapshot,
            score_improvement=score_diff,
            gaps_closed=gaps_to_close,
            new_capabilities_unlocked=unlocked,
            simulation_verdict=verdict
        )

simulation_agent = FutureCareerSimulationAgent()
