from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ..models.profile import StudentProfile
from ..models.agents import (
    OrchestrationResult,
    SimulationRequest,
    SimulationAgentOutput,
    ProfileAgentOutput,
    SkillGapAgentOutput,
    CareerRoadmapAgentOutput,
    ProjectAgentOutput,
    CareerStrategistAgentOutput,
    CareerGoalUpdateRequest
)
from ..services.storage import storage_service
from ..services.resume_parser import parse_resume_file
from ..agents.orchestrator import orchestrator
from ..agents.profile_agent import profile_agent
from ..agents.skill_gap_agent import skill_gap_agent
from ..agents.roadmap_agent import roadmap_agent
from ..agents.project_agent import project_agent
from ..agents.simulation_agent import simulation_agent
from ..agents.strategist_agent import strategist_agent
from ..data.role_benchmarks import get_all_roles, ROLE_BENCHMARKS
from ..data.sample_profiles import SAMPLE_PROFILES, get_sample_profile
from ..config import GEMINI_API_KEY, GEMINI_MODEL

router = APIRouter(prefix="/api", tags=["CareerTwin AI"])

# ----------------- Status & Mode ----------------- #

@router.get("/status")
async def get_system_status():
    is_live = bool(GEMINI_API_KEY)
    return {
        "service": "CareerTwin AI",
        "mode": "Live Google Gemini Mode" if is_live else "Demo Mode (Realistic Heuristic AI)",
        "is_demo_mode": not is_live,
        "model": GEMINI_MODEL if is_live else "Deterministic Multi-Agent Heuristic Engine",
        "has_api_key": is_live
    }

# ----------------- Profile Endpoints ----------------- #

@router.get("/profile", response_model=StudentProfile)
async def get_current_profile():
    profile = storage_service.get_profile("default_student")
    if not profile:
        profile = StudentProfile(id="default_student", name="", target_career="Software Engineer")
        storage_service.save_profile(profile)
    return profile

@router.post("/profile", response_model=StudentProfile)
async def update_profile(profile: StudentProfile):
    profile.id = "default_student"

    # Recalculate deterministic profile analysis
    profile_out = profile_agent.analyze_profile(profile)
    profile.readiness_score = profile_out.readiness_estimate

    # Save the updated student profile
    saved = storage_service.save_profile(profile)

    # Run all agents with the updated profile
    result = orchestrator.execute_pipeline(saved)

    # Replace the cached results
    storage_service.save_state("latest_orchestration", result.model_dump())

    return saved

@router.post("/profile/reset")
async def reset_profile():
    """Clears uploaded resume, target JD, skills and resets profile for a clean fresh analysis."""
    empty_profile = StudentProfile(
        id="default_student",
        name="",
        degree="B.Tech",
        branch="Computer Science Engineering",
        year_of_study="3rd Year",
        cgpa=None,
        current_skills=[],
        projects=[],
        certifications=[],
        career_interests=[],
        target_career="Software Engineer",
        dream_company="",
        job_description="",
        resume_filename="",
        raw_resume_text="",
        readiness_score=0.0
    )
    saved = storage_service.save_profile(empty_profile)
    result = orchestrator.execute_pipeline(saved)
    storage_service.save_state("latest_orchestration", result.model_dump())
    return {
        "message": "Profile reset successfully. Ready for a new career analysis.",
        "profile": saved,
        "orchestration": result
    }

# ----------------- Resume Upload ----------------- #

@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT resume files are supported.")
    
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Parse resume
    parsed_data = parse_resume_file(file_bytes, filename=file.filename)
    if not parsed_data:
        raise HTTPException(status_code=400, detail="Could not extract text from the uploaded resume.")

    # Fetch existing profile to preserve custom Target Role / JD if already set
    current_profile = storage_service.get_profile("default_student") or StudentProfile(id="default_student", name="", target_career="Software Engineer")
    
    # Merge extracted data into current profile
    if parsed_data.get("name"):
        current_profile.name = parsed_data["name"]
    if parsed_data.get("current_skills"):
        current_profile.current_skills = parsed_data["current_skills"]
    if parsed_data.get("projects"):
        current_profile.projects = parsed_data["projects"]
    if parsed_data.get("certifications"):
        current_profile.certifications = parsed_data["certifications"]
    if parsed_data.get("degree"):
        current_profile.degree = parsed_data["degree"]
    if parsed_data.get("branch"):
        current_profile.branch = parsed_data["branch"]
    if parsed_data.get("cgpa"):
        current_profile.cgpa = parsed_data["cgpa"]
    if parsed_data.get("year_of_study"):
        current_profile.year_of_study = parsed_data["year_of_study"]
    
    current_profile.resume_filename = file.filename
    current_profile.raw_resume_text = parsed_data.get("raw_resume_text", "")

    # Recalculate deterministic readiness score
    profile_out = profile_agent.analyze_profile(current_profile)
    current_profile.readiness_score = profile_out.readiness_estimate

    # Save profile
    saved = storage_service.save_profile(current_profile)

    # Run full orchestration pipeline
    result = orchestrator.execute_pipeline(saved)
    storage_service.save_state("latest_orchestration", result.model_dump())

    return {
        "message": f"Resume '{file.filename}' processed successfully!",
        "filename": file.filename,
        "profile": saved,
        "orchestration": result
    }

# ----------------- Career Goal & JD Update ----------------- #

@router.post("/career-goal", response_model=OrchestrationResult)
async def update_career_goal(payload: CareerGoalUpdateRequest):
    profile = storage_service.get_profile("default_student") or StudentProfile(id="default_student", name="", target_career="Software Engineer")
    
    profile.target_career = payload.target_career.strip() if payload.target_career else "Software Engineer"
    profile.job_description = payload.job_description.strip() if payload.job_description else ""

    # Recalculate deterministic profile analysis
    profile_out = profile_agent.analyze_profile(profile)
    profile.readiness_score = profile_out.readiness_estimate

    saved = storage_service.save_profile(profile)

    # Run full orchestration pipeline
    result = orchestrator.execute_pipeline(saved)
    storage_service.save_state("latest_orchestration", result.model_dump())

    return result

# ----------------- Sample Profiles ----------------- #

@router.post("/profile/sample/{sample_id}", response_model=StudentProfile)
async def load_sample_profile(sample_id: str):
    if sample_id not in SAMPLE_PROFILES:
        sample_id = "revathi_ai" if "revathi_ai" in SAMPLE_PROFILES else "demo_student"
    sample = get_sample_profile(sample_id)
    sample.id = "default_student"
    saved = storage_service.save_profile(sample)
    
    # Run orchestration for the loaded profile immediately
    result = orchestrator.execute_pipeline(saved)
    storage_service.save_state("latest_orchestration", result.model_dump())
    return saved

# ----------------- Roles ----------------- #

@router.get("/roles")
async def get_roles():
    roles = []
    for title, data in ROLE_BENCHMARKS.items():
        roles.append({
            "title": title,
            "description": data["description"],
            "core_skills": data["core_skills"][:6]
        })
    return roles

# ----------------- Multi-Agent Orchestration ----------------- #

@router.post("/orchestrate", response_model=OrchestrationResult)
async def run_full_orchestration():
    profile = storage_service.get_profile("default_student")
    if not profile:
        profile = StudentProfile(id="default_student", name="", target_career="Software Engineer")
        storage_service.save_profile(profile)

    result = orchestrator.execute_pipeline(profile)
    storage_service.save_state("latest_orchestration", result.model_dump())
    return result

@router.get("/orchestrate/latest", response_model=OrchestrationResult)
async def get_latest_orchestration():
    profile = storage_service.get_profile("default_student")
    if not profile or (not profile.current_skills and not profile.projects and not profile.resume_filename):
        empty_prof = profile or StudentProfile(id="default_student", name="", target_career="Software Engineer", readiness_score=0.0)
        result = orchestrator.execute_pipeline(empty_prof)
        return result

    cached = storage_service.get_state("latest_orchestration")
    if cached:
        return OrchestrationResult(**cached)
    
    result = orchestrator.execute_pipeline(profile)
    storage_service.save_state("latest_orchestration", result.model_dump())
    return result

# ----------------- Future Career Simulation ----------------- #

@router.post("/twin/simulate", response_model=SimulationAgentOutput)
async def run_future_simulation(payload: SimulationRequest):
    profile = storage_service.get_profile("default_student") or StudentProfile(id="default_student", name="", target_career="Software Engineer")
    gap_out = skill_gap_agent.analyze_gaps(profile)
    
    sim_result = simulation_agent.simulate_future(
        profile=profile,
        gap_output=gap_out,
        selected_actions=payload.actions,
        custom_scenario=payload.custom_scenario
    )

    # Update latest orchestration state with the new simulation output
    cached = storage_service.get_state("latest_orchestration")
    if cached:
        cached["simulation_output"] = sim_result.model_dump()
        storage_service.save_state("latest_orchestration", cached)

    return sim_result
