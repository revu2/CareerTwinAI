from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid

# Detailed Realistic Readiness Score Breakdown (40/25/15/20 Model)
class ReadinessScoreBreakdown(BaseModel):
    required_skills_score: float = 0.0      # Max 40.0 pts (40% weight)
    projects_experience_score: float = 0.0  # Max 25.0 pts (25% weight)
    education_certs_score: float = 0.0      # Max 15.0 pts (15% weight)
    role_gaps_score: float = 0.0            # Max 20.0 pts (20% weight)
    total_score: float = 48.0               # Max 100.0 pts
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    score_explanation: str = ""
    improvement_recommendations: List[str] = Field(default_factory=list)

# 1. Digital Twin / Profile Agent Output
class ProfileAgentOutput(BaseModel):
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    career_stage: str = "Early Intermediate / Pre-Specialization"
    readiness_estimate: float = 48.0
    breakdown: Optional[ReadinessScoreBreakdown] = Field(default_factory=ReadinessScoreBreakdown)

# 2. Skill Gap Agent Output
class CategorizedSkillItem(BaseModel):
    name: str
    category: str  # "Strong", "Developing", "Missing"
    priority: Optional[str] = "Normal"  # "High", "Medium", "Normal"
    importance_reason: Optional[str] = ""

class SkillGapAgentOutput(BaseModel):
    target_role: str
    overall_match_percentage: float = 48.0
    required_skills: List[str] = Field(default_factory=list)
    current_skills: List[str] = Field(default_factory=list)
    strong_skills: List[str] = Field(default_factory=list)
    developing_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    priority_skills: List[str] = Field(default_factory=list)
    radar_data: Dict[str, Any] = Field(default_factory=dict)

# 3. Career Roadmap Agent Output (5 Phases)
class RoadmapPhase(BaseModel):
    phase_number: int
    phase_name: str
    timeframe: str
    skills_to_learn: List[str] = Field(default_factory=list)
    suggested_activities: List[str] = Field(default_factory=list)
    expected_outcome: str

class CareerRoadmapAgentOutput(BaseModel):
    target_role: str
    phases: List[RoadmapPhase] = Field(default_factory=list)
    estimated_timeline: str = "6 Months (12-15 hrs/week)"

# 4. Project and Experience Agent Output
class ProjectRecommendation(BaseModel):
    title: str
    difficulty: str  # "Beginner", "Intermediate", "Advanced"
    skills_gained: List[str] = Field(default_factory=list)
    why_it_helps: str
    architecture_overview: str
    deliverable: str

class ProjectAgentOutput(BaseModel):
    target_role: str
    recommended_projects: List[ProjectRecommendation] = Field(default_factory=list)
    portfolio_activities: List[str] = Field(default_factory=list)
    internship_preparation_areas: List[str] = Field(default_factory=list)

# 5. Career Strategist Agent Output
class CareerStrategistAgentOutput(BaseModel):
    current_career_assessment: str
    top_strengths: List[str] = Field(default_factory=list)
    biggest_gaps: List[str] = Field(default_factory=list)
    immediate_next_steps: List[str] = Field(default_factory=list)
    short_term_strategy: List[str] = Field(default_factory=list)
    long_term_strategy: List[str] = Field(default_factory=list)
    action_priority_matrix: Dict[str, str] = Field(default_factory=dict)

# 6. Future Career Simulation Agent Output (The Unique Feature)
class TwinStateSnapshot(BaseModel):
    title: str
    readiness_score: float
    skills_summary: List[str]
    projects_count: int
    strengths_highlight: str
    unresolved_gaps: List[str]
    competitive_tier: str

class SimulationAgentOutput(BaseModel):
    selected_actions: List[str]
    custom_scenario: Optional[str] = ""
    current_twin: TwinStateSnapshot
    future_simulated_twin: TwinStateSnapshot
    score_improvement: float
    gaps_closed: List[str]
    new_capabilities_unlocked: List[str]
    simulation_verdict: str
    disclaimer: str = (
        "AI-Generated Simulation Estimate: These results reflect heuristic AI career modelling "
        "and skill acquisition trajectories, not a guaranteed offer of employment or salary."
    )

# Individual Agent Trace in the Orchestrator Pipeline
class AgentTrace(BaseModel):
    agent_id: str
    agent_name: str
    role_description: str
    status: str = "Completed"  # "Pending", "In Progress", "Completed"
    input_summary: str
    reasoning_analysis: str
    output_summary: str
    full_output: Dict[str, Any] = Field(default_factory=dict)

# Full Orchestration Result
class OrchestrationResult(BaseModel):
    student_name: str
    target_role: str
    is_demo_mode: bool = True
    executed_agents: List[AgentTrace] = Field(default_factory=list)
    profile_agent_output: ProfileAgentOutput
    skill_gap_output: SkillGapAgentOutput
    roadmap_output: CareerRoadmapAgentOutput
    project_output: ProjectAgentOutput
    simulation_output: SimulationAgentOutput
    strategist_output: CareerStrategistAgentOutput

# What-If Simulation Request
class SimulationRequest(BaseModel):
    actions: List[str] = Field(default_factory=list)
    custom_scenario: Optional[str] = ""

# Target Career & JD Update Request
class CareerGoalUpdateRequest(BaseModel):
    target_career: str
    job_description: Optional[str] = ""
