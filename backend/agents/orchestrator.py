from typing import Dict, Any, List, Optional
import time
from ..models.profile import StudentProfile
from ..models.agents import (
    OrchestrationResult,
    AgentTrace,
    SimulationRequest
)
from .profile_agent import profile_agent
from .skill_gap_agent import skill_gap_agent
from .roadmap_agent import roadmap_agent
from .project_agent import project_agent
from .simulation_agent import simulation_agent
from .strategist_agent import strategist_agent
from ..config import GEMINI_API_KEY

class AIOrchestrator:
    """
    AI Orchestrator that coordinates the multi-agent career strategy pipeline:
    Student Profile 
         ↓
    Digital Twin / Profile Agent (Agent 1)
         ↓
    Skill Gap Agent (Agent 2)
         ↓
    Career Roadmap Agent (Agent 3)
         ↓
    Project & Experience Agent (Agent 4)
         ↓
    Future Simulation Agent (Agent 6)
         ↓
    Career Strategist Agent (Agent 5)
         ↓
    Final Master Career Strategy Report
    """
    def __init__(self):
        self.name = "AI Career Orchestrator"

    def execute_pipeline(
        self,
        profile: StudentProfile,
        sim_actions: Optional[List[str]] = None,
        custom_scenario: Optional[str] = ""
    ) -> OrchestrationResult:
        is_demo_mode = not bool(GEMINI_API_KEY)
        traces: List[AgentTrace] = []
        display_name = profile.name.strip() if profile.name and profile.name.strip() else "Your Career Twin"

        # --- STEP 1: Digital Twin / Profile Agent ---
        start_t = time.time()
        profile_out = profile_agent.analyze_profile(profile)
        # Update composite readiness score on profile
        profile.readiness_score = profile_out.readiness_estimate
        traces.append(AgentTrace(
            agent_id="agent_1_profile",
            agent_name="Digital Twin / Profile Agent",
            role_description="Creates a structured digital replica of the student's career state and identifies foundational strengths & weaknesses.",
            status="Completed",
            input_summary=f"Profile: {display_name}, {profile.degree} in {profile.branch}, Skills: {', '.join(profile.get_skills_list()[:4])}",
            reasoning_analysis=f"Evaluated academic trajectory, coursework, and initial projects. Student is at '{profile_out.career_stage}'.",
            output_summary=f"Readiness Score: {profile_out.readiness_estimate}/100. Identified {len(profile_out.strengths)} strengths and {len(profile_out.weaknesses)} growth areas.",
            full_output=profile_out.model_dump()
        ))

        # --- STEP 2: Skill Gap Agent ---
        start_t = time.time()
        gap_out = skill_gap_agent.analyze_gaps(profile)
        traces.append(AgentTrace(
            agent_id="agent_2_skill_gap",
            agent_name="Skill Gap Agent",
            role_description="Benchmarks student skills against industry requirements and categorizes them into Strong, Developing, and Missing.",
            status="Completed",
            input_summary=f"Target Role: {profile.target_career}, Current Skills: {len(profile.get_skills_list())}",
            reasoning_analysis=f"Benchmarked skills against role standards. Detected {len(gap_out.missing_skills)} missing skills. Priority: {', '.join(gap_out.priority_skills[:2])}.",
            output_summary=f"Overall Role Match: {gap_out.overall_match_percentage}%. Classified {len(gap_out.strong_skills)} Strong, {len(gap_out.developing_skills)} Developing, and {len(gap_out.missing_skills)} Missing skills.",
            full_output=gap_out.model_dump()
        ))

        # --- STEP 3: Career Roadmap Agent ---
        start_t = time.time()
        roadmap_out = roadmap_agent.generate_roadmap(profile, gap_out)
        traces.append(AgentTrace(
            agent_id="agent_3_roadmap",
            agent_name="Career Roadmap Agent",
            role_description="Transforms skill gap insights into a structured 5-phase personalized learning and upskilling curriculum.",
            status="Completed",
            input_summary=f"Missing Skills: {', '.join(gap_out.missing_skills[:3])}, Target: {profile.target_career}",
            reasoning_analysis="Constructed 5 progressive phases: Foundation -> Core Skills -> Advanced Skills -> Projects & Portfolio -> Interview Prep.",
            output_summary=f"Generated 5-Phase Roadmap spanning {roadmap_out.estimated_timeline} with concrete milestones and deliverables.",
            full_output=roadmap_out.model_dump()
        ))

        # --- STEP 4: Project & Experience Agent ---
        start_t = time.time()
        project_out = project_agent.recommend_projects(profile, gap_out)
        traces.append(AgentTrace(
            agent_id="agent_4_projects",
            agent_name="Project & Experience Agent",
            role_description="Recommends practical, high-yield portfolio projects and portfolio-building activities.",
            status="Completed",
            input_summary=f"Target Role: {profile.target_career}, Missing Capabilities: {', '.join(gap_out.missing_skills[:3])}",
            reasoning_analysis="Designed 3 production-grade portfolio architectures that prove practical capability to hiring managers.",
            output_summary=f"Recommended {len(project_out.recommended_projects)} flagship projects with full system architectures and portfolio guidelines.",
            full_output=project_out.model_dump()
        ))

        # --- STEP 5: Future Career Simulation Agent ---
        start_t = time.time()
        default_actions = [
            "Learn Machine Learning & Deep Learning (PyTorch, TensorFlow)",
            "Build & Deploy 2 Production AI Projects (RAG & Computer Vision)",
            "Master Docker Containerization & FastAPI Model Serving"
        ]
        chosen_actions = sim_actions if (sim_actions and len(sim_actions) > 0) else default_actions
        simulation_out = simulation_agent.simulate_future(profile, gap_out, chosen_actions, custom_scenario)
        traces.append(AgentTrace(
            agent_id="agent_6_simulation",
            agent_name="Future Career Simulation Agent",
            role_description="Simulates hypothetical career improvements and compares Current Digital Twin vs Future Simulated Twin.",
            status="Completed",
            input_summary=f"Selected {len(chosen_actions)} hypothetical upskilling actions: {chosen_actions[0]}...",
            reasoning_analysis=f"Projected impact of closing {len(simulation_out.gaps_closed)} skill gaps. Twin readiness projected to increase by +{simulation_out.score_improvement}%.",
            output_summary=f"Current Twin ({simulation_out.current_twin.readiness_score}%) -> Future Simulated Twin ({simulation_out.future_simulated_twin.readiness_score}%). Competitive Tier: '{simulation_out.future_simulated_twin.competitive_tier}'.",
            full_output=simulation_out.model_dump()
        ))

        # --- STEP 6: Career Strategist Agent ---
        start_t = time.time()
        strategist_out = strategist_agent.formulate_strategy(
            profile=profile,
            profile_out=profile_out,
            gap_out=gap_out,
            roadmap_out=roadmap_out,
            project_out=project_out,
            simulation_out=simulation_out
        )
        traces.append(AgentTrace(
            agent_id="agent_5_strategist",
            agent_name="Career Strategist Agent",
            role_description="Synthesizes intelligence from all agents to formulate a personalized master career strategy.",
            status="Completed",
            input_summary="Synthesized findings from Profile, Gap, Roadmap, Project, and Simulation Agents.",
            reasoning_analysis="Formulated immediate 14-day quick wins, short-term build phases, and long-term placement strategy.",
            output_summary=f"Formulated Master Strategy with {len(strategist_out.immediate_next_steps)} immediate steps, short-term plans, and priority matrix.",
            full_output=strategist_out.model_dump()
        ))

        return OrchestrationResult(
            student_name=display_name,
            target_role=profile.target_career,
            is_demo_mode=is_demo_mode,
            executed_agents=traces,
            profile_agent_output=profile_out,
            skill_gap_output=gap_out,
            roadmap_output=roadmap_out,
            project_output=project_out,
            simulation_output=simulation_out,
            strategist_output=strategist_out
        )

orchestrator = AIOrchestrator()
