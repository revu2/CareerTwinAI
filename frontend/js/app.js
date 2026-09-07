/**
 * CareerTwin AI - Frontend Application Core
 * Autonomous Multi-Agent AI Career Digital Twin Platform
 */

const API_BASE = '/api';

// Global State
const state = {
  currentTab: 'dashboard',
  profile: null,
  orchestrationData: null,
  systemStatus: null,
  radarChartInstance: null,
  selectedSimActions: [
    "Learn Machine Learning & Deep Learning (PyTorch, TensorFlow)",
    "Build & Deploy 2 Production AI Projects (RAG & Computer Vision)",
    "Master Docker Containerization & FastAPI Model Serving"
  ],
};

// Initialize app on DOM load
document.addEventListener('DOMContentLoaded', async () => {
  try {
    sessionStorage.clear();
    localStorage.clear();
  } catch (e) {}

  initLucide();
  setupNavigation();
  setupEventListeners();
  await checkSystemStatus();
  await resetProfileToNewAnalysis(true);
});

function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// ----------------- System Status ----------------- //

async function checkSystemStatus() {
  try {
    const res = await fetch(`${API_BASE}/status`);
    if (res.ok) {
      state.systemStatus = await res.json();
    }
  } catch (err) {
    console.warn('Could not fetch system status:', err);
  }
}

// ----------------- Navigation ----------------- //

function setupNavigation() {
  const tabButtons = document.querySelectorAll('.nav-tab');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  state.currentTab = tabId;
  document.querySelectorAll('.nav-tab').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });

  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('hidden', content.id !== `tab-${tabId}`);
  });

  if (tabId === 'dashboard') {
    renderDashboard();
  } else if (tabId === 'roadmap') {
    renderRoadmapView();
  } else if (tabId === 'projects') {
    renderProjectsView();
  } else if (tabId === 'simulation') {
    renderSimulationView();
  } else if (tabId === 'strategy') {
    renderStrategyReport();
  } else if (tabId === 'profile') {
    populateProfileForm();
  }

  initLucide();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ----------------- Data Orchestration ----------------- //

async function refreshAll() {
  showLoader(true, "Synchronizing Career Digital Twin...");
  try {
    const res = await fetch(`${API_BASE}/orchestrate/latest`);
    if (res.ok) {
      state.orchestrationData = await res.json();
      state.profile = await (await fetch(`${API_BASE}/profile`)).json();
      updateHeaderProfileInfo();
      renderDashboard();
    }
  } catch (err) {
    showToast('Failed to load CareerTwin data', 'error');
  } finally {
    showLoader(false);
  }
}

async function triggerOrchestration() {
  showLoader(true, "Orchestrating 6 AI specialized agents...");
  try {
    const res = await fetch(`${API_BASE}/orchestrate`, { method: 'POST' });
    if (res.ok) {
      state.orchestrationData = await res.json();
      state.profile = await (await fetch(`${API_BASE}/profile`)).json();
      updateHeaderProfileInfo();
      showToast('Career Digital Twin synchronized!', 'success');
      switchTab('dashboard');
    }
  } catch (err) {
    showToast('Error during career orchestration', 'error');
  } finally {
    showLoader(false);
  }
}

function updateHeaderProfileInfo() {
  if (!state.profile) return;
  const targetRole = state.profile.target_career || "Software Engineer";
  const score = Math.round(state.profile.readiness_score || 0);

  const roleEl = document.getElementById('headerTargetRole');
  if (roleEl) roleEl.textContent = targetRole;

  const badgeEl = document.getElementById('headerReadinessBadge');
  if (badgeEl) {
    badgeEl.textContent = score > 0 ? `${score}% Readiness` : `0% (Ready)`;
  }
}

// ----------------- 1. Target Role & JD Editing ----------------- //

function handleTargetRoleSelectChange(val) {
  const customInput = document.getElementById('quickCustomRoleInput');
  const roleEl = document.getElementById('headerTargetRole');
  const targetGoalEl = document.getElementById('dashTargetGoal');

  if (val === 'custom') {
    if (customInput) {
      customInput.classList.remove('hidden');
      customInput.focus();
      const currentCustom = customInput.value.trim() || "Custom Role";
      if (roleEl) roleEl.textContent = currentCustom;
      if (targetGoalEl) targetGoalEl.textContent = currentCustom;
    }
  } else {
    if (customInput) customInput.classList.add('hidden');
    if (roleEl) roleEl.textContent = val;
    if (targetGoalEl) targetGoalEl.textContent = val;
    if (state.profile) state.profile.target_career = val;
  }
}

async function analyzeCareerReadiness() {
  const selectEl = document.getElementById('quickTargetRoleSelect');
  const customEl = document.getElementById('quickCustomRoleInput');
  const jdEl = document.getElementById('quickJobDescriptionInput');

  let targetRole = selectEl ? selectEl.value : "Software Engineer";
  if (targetRole === 'custom') {
    targetRole = (customEl && customEl.value.trim()) ? customEl.value.trim() : "Software Engineer";
  }

  const jdText = jdEl ? jdEl.value.trim() : "";

  showLoader(true, `Analyzing readiness for '${targetRole}' against JD requirements...`);
  try {
    const res = await fetch(`${API_BASE}/career-goal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_career: targetRole,
        job_description: jdText
      })
    });

    if (res.ok) {
      const data = await res.json();
      state.orchestrationData = data;
      state.profile = await (await fetch(`${API_BASE}/profile`)).json();
      updateHeaderProfileInfo();
      renderDashboard();
      if (window.confetti) {
        window.confetti({ particleCount: 40, spread: 65, origin: { y: 0.6 } });
      }
      showToast(`Career readiness analyzed for ${targetRole}!`, 'success');
    } else {
      const err = await res.json();
      showToast(err.detail || 'Failed to update target role analysis', 'error');
    }
  } catch (err) {
    showToast('Error connecting to AI analysis server', 'error');
  } finally {
    showLoader(false);
  }
}

// ----------------- 2. PDF Resume Upload ----------------- //

async function handleResumeFileUpload(event) {
  const fileInput = document.getElementById('resumeFileInput');
  const file = (event && event.target && event.target.files && event.target.files[0]) || (fileInput && fileInput.files && fileInput.files[0]);
  
  if (!file) return;

  const btnText = document.getElementById('uploadResumeBtnText');
  if (btnText) btnText.textContent = `Uploading ${file.name}...`;

  const formData = new FormData();
  formData.append('file', file);

  showLoader(true, `Extracting and analyzing text from '${file.name}'...`);
  try {
    const res = await fetch(`${API_BASE}/resume/upload`, {
      method: 'POST',
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      state.profile = data.profile;
      state.orchestrationData = data.orchestration;
      sessionStorage.setItem('active_session_upload', file.name);
      updateHeaderProfileInfo();
      renderDashboard();
      if (window.confetti) {
        window.confetti({ particleCount: 50, spread: 70, origin: { y: 0.6 } });
      }
      showToast(`Resume '${file.name}' parsed successfully!`, 'success');
    } else {
      const errData = await res.json();
      showToast(errData.detail || 'Failed to parse resume PDF', 'error');
      if (btnText) btnText.textContent = `Select Resume PDF`;
    }
  } catch (err) {
    showToast('Error uploading resume file', 'error');
    if (btnText) btnText.textContent = `Select Resume PDF`;
  } finally {
    showLoader(false);
    if (fileInput) fileInput.value = '';
  }
}

// ----------------- 3. New Analysis / Clear Profile ----------------- //

async function resetProfileToNewAnalysis(silent = false) {
  showLoader(true, silent ? "Initializing fresh session..." : "Clearing profile for fresh analysis...");
  try {
    const res = await fetch(`${API_BASE}/profile/reset`, { method: 'POST' });
    if (res.ok) {
      const data = await res.json();
      state.profile = data.profile;
      state.orchestrationData = data.orchestration;
      sessionStorage.removeItem('active_session_upload');

      // Clear input controls
      const jdEl = document.getElementById('quickJobDescriptionInput');
      if (jdEl) jdEl.value = '';

      const selectEl = document.getElementById('quickTargetRoleSelect');
      if (selectEl) selectEl.value = 'Software Engineer';

      const customEl = document.getElementById('quickCustomRoleInput');
      if (customEl) {
        customEl.value = '';
        customEl.classList.add('hidden');
      }

      updateHeaderProfileInfo();
      renderDashboard();
      if (!silent) {
        showToast('Profile cleared. Ready for a new career analysis.', 'info');
      }
    } else {
      if (!silent) showToast('Failed to reset profile', 'error');
    }
  } catch (err) {
    if (!silent) showToast('Error resetting profile', 'error');
  } finally {
    showLoader(false);
  }
}

// ----------------- 4. Clean Unified Dashboard View ----------------- //

function renderDashboard() {
  if (!state.orchestrationData || !state.profile) return;
  const data = state.orchestrationData;
  const prof = state.profile;
  const pOut = data.profile_agent_output;
  const gapOut = data.skill_gap_output;
  const simOut = data.simulation_output;
  const stratOut = data.strategist_output;
  const roadmapOut = data.roadmap_output;
  const projectOut = data.project_output;
  const breakdown = pOut.breakdown || {
    required_skills_score: 0.0,
    projects_experience_score: 0.0,
    education_certs_score: 0.0,
    role_gaps_score: 0.0,
    total_score: pOut.readiness_estimate || 0.0,
    score_explanation: "Deterministic readiness evaluation across 4 dimensions.",
    improvement_recommendations: []
  };

  // TOP CONTROL HUB: Sync inputs
  const selectEl = document.getElementById('quickTargetRoleSelect');
  const customEl = document.getElementById('quickCustomRoleInput');
  const jdEl = document.getElementById('quickJobDescriptionInput');
  const resumeBadgeContainer = document.getElementById('resumeStatusBadgeContainer');
  const uploadBtnText = document.getElementById('uploadResumeBtnText');

  const standardRoles = ["Software Engineer", "AI Engineer", "Fullstack Software Engineer", "Data Scientist", "DevOps & Cloud Engineer", "Backend Engineer", "Machine Learning Engineer", "Cybersecurity Analyst"];
  if (selectEl && prof.target_career) {
    if (standardRoles.includes(prof.target_career)) {
      selectEl.value = prof.target_career;
      if (customEl) customEl.classList.add('hidden');
    } else {
      selectEl.value = "custom";
      if (customEl) {
        customEl.classList.remove('hidden');
        customEl.value = prof.target_career;
      }
    }
  }

  if (jdEl && prof.job_description !== undefined) {
    jdEl.value = prof.job_description || "";
  }

  // Resume status badge
  if (resumeBadgeContainer) {
    if (prof.resume_filename) {
      resumeBadgeContainer.innerHTML = `
        <span class="text-[11px] px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5 font-semibold">
          <i data-lucide="file-check" class="w-3.5 h-3.5 text-emerald-400"></i> ${prof.resume_filename}
        </span>
      `;
      if (uploadBtnText) uploadBtnText.textContent = `Replace Resume PDF`;
    } else {
      resumeBadgeContainer.innerHTML = `
        <span class="text-[11px] px-3 py-1 rounded-full bg-slate-900 text-slate-400 border border-slate-800 flex items-center gap-1.5">
          <i data-lucide="file" class="w-3.5 h-3.5 text-slate-500"></i> No resume uploaded
        </span>
      `;
      if (uploadBtnText) uploadBtnText.textContent = `Select Resume PDF`;
    }
  }

  // SECTION 1: Career Overview
  const hasName = prof.name && prof.name.trim();
  const twinGreeting = hasName ? `${prof.name.trim()}'s Career Digital Twin` : "Your Career Digital Twin";
  const greetingEl = document.getElementById('dashCandidateGreeting');
  if (greetingEl) greetingEl.textContent = twinGreeting;

  const branchText = prof.branch ? ` in ${prof.branch}` : '';
  const yearText = prof.year_of_study ? ` • ${prof.year_of_study}` : '';
  const degreeEl = document.getElementById('dashProfileDegree');
  if (degreeEl) degreeEl.textContent = `${prof.degree || 'B.Tech'}${branchText}${yearText}`;

  const summaryEl = document.getElementById('dashProfileSummary');
  if (summaryEl) summaryEl.textContent = pOut.summary;

  // SECTION 2: AI-Estimated Readiness Score
  const scoreEl = document.getElementById('dashReadinessScore');
  if (scoreEl) {
    scoreEl.textContent = `${Math.round(pOut.readiness_estimate || 0)}%`;
  }

  const stageEl = document.getElementById('dashCareerStageBadge');
  if (stageEl) stageEl.textContent = pOut.career_stage;

  const targetEl = document.getElementById('dashTargetGoal');
  if (targetEl) targetEl.textContent = prof.target_career || "Software Engineer";

  // SECTION 2 BREAKDOWN CARDS (40 / 25 / 15 / 20 Model)
  const skillsScoreEl = document.getElementById('scorePartSkills');
  const barSkillsEl = document.getElementById('barPartSkills');
  if (skillsScoreEl && barSkillsEl) {
    skillsScoreEl.textContent = `${(breakdown.required_skills_score || 0).toFixed(1)} / 40`;
    barSkillsEl.style.width = `${Math.min(((breakdown.required_skills_score || 0) / 40) * 100, 100)}%`;
  }

  const projScoreEl = document.getElementById('scorePartProjects');
  const barProjEl = document.getElementById('barPartProjects');
  if (projScoreEl && barProjEl) {
    projScoreEl.textContent = `${(breakdown.projects_experience_score || 0).toFixed(1)} / 25`;
    barProjEl.style.width = `${Math.min(((breakdown.projects_experience_score || 0) / 25) * 100, 100)}%`;
  }

  const eduScoreEl = document.getElementById('scorePartEdu');
  const barEduEl = document.getElementById('barPartEdu');
  if (eduScoreEl && barEduEl) {
    eduScoreEl.textContent = `${(breakdown.education_certs_score || 0).toFixed(1)} / 15`;
    barEduEl.style.width = `${Math.min(((breakdown.education_certs_score || 0) / 15) * 100, 100)}%`;
  }

  const gapsScoreEl = document.getElementById('scorePartGaps');
  const barGapsEl = document.getElementById('barPartGaps');
  if (gapsScoreEl && barGapsEl) {
    gapsScoreEl.textContent = `${(breakdown.role_gaps_score || 0).toFixed(1)} / 20`;
    barGapsEl.style.width = `${Math.min(((breakdown.role_gaps_score || 0) / 20) * 100, 100)}%`;
  }

  // Explanation & Recommendations
  const explainEl = document.getElementById('scoreExplanationText');
  if (explainEl) explainEl.textContent = breakdown.score_explanation || pOut.summary;

  const recListEl = document.getElementById('scoreRecommendationsList');
  if (recListEl && breakdown.improvement_recommendations) {
    recListEl.innerHTML = breakdown.improvement_recommendations.map(r => `
      <li class="flex items-start gap-2">
        <span class="text-emerald-400 font-bold">➔</span>
        <span>${r}</span>
      </li>
    `).join('');
  }

  // SECTION 3: Current Skills & Skill Gaps
  const strengthsContainer = document.getElementById('dashTopStrengths');
  if (strengthsContainer) {
    if (pOut.strengths && pOut.strengths.length > 0) {
      strengthsContainer.innerHTML = pOut.strengths.slice(0, 4).map(s => `
        <li class="flex items-start gap-2.5 text-xs text-slate-200">
          <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
          <span>${s}</span>
        </li>
      `).join('');
    } else {
      strengthsContainer.innerHTML = `
        <li class="text-xs text-slate-400">Upload your PDF resume to verify skills.</li>
      `;
    }
  }

  const gapsContainer = document.getElementById('dashMajorGaps');
  if (gapsContainer) {
    gapsContainer.innerHTML = (gapOut.priority_skills || gapOut.missing_skills || []).slice(0, 4).map(g => `
      <li class="flex items-start gap-2.5 text-xs text-slate-200">
        <i data-lucide="flame" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i>
        <span class="font-medium text-rose-200">${g}</span>
      </li>
    `).join('');
  }

  renderRadarChart('dashRadarChartCanvas', gapOut.radar_data);

  // SECTION 4: 5-Phase Roadmap Summary
  const roadmapContainer = document.getElementById('dashRoadmapSummaryContainer');
  if (roadmapContainer && roadmapOut && roadmapOut.phases) {
    roadmapContainer.innerHTML = roadmapOut.phases.map(p => `
      <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between text-[11px] mb-1">
            <span class="font-bold text-indigo-400">Phase 0${p.phase_number}</span>
            <span class="text-slate-400 text-[10px]">${p.timeframe}</span>
          </div>
          <h4 class="text-xs font-bold text-white leading-tight">${p.phase_name.replace(/^Phase \d+:\s*/i, '')}</h4>
        </div>
        <div class="text-[11px] text-slate-300 pt-1 border-t border-slate-800/80">
          <span class="text-[10px] font-semibold text-cyan-400 block mb-0.5">Key Focus:</span>
          <span class="truncate block text-slate-300">${p.skills_to_learn.slice(0, 2).join(', ')}</span>
        </div>
      </div>
    `).join('');
  }

  // SECTION 5: Immediate Next Steps & Project Highlights
  const stepsContainer = document.getElementById('dashImmediateStepsList');
  if (stepsContainer && stratOut && stratOut.immediate_next_steps) {
    stepsContainer.innerHTML = stratOut.immediate_next_steps.slice(0, 3).map((step, idx) => `
      <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-2.5 text-xs text-slate-200">
        <span class="w-5 h-5 rounded-lg bg-indigo-600/30 text-indigo-300 font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">
          ${idx + 1}
        </span>
        <span class="leading-relaxed">${step}</span>
      </div>
    `).join('');
  }

  const projContainer = document.getElementById('dashProjectHighlightsContainer');
  if (projContainer && projectOut && projectOut.recommended_projects) {
    projContainer.innerHTML = projectOut.recommended_projects.slice(0, 2).map(p => `
      <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between text-[10px] mb-1">
            <span class="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-bold">${p.difficulty}</span>
            <span class="text-slate-400">Flagship Portfolio</span>
          </div>
          <h4 class="text-xs font-bold text-white">${p.title}</h4>
          <p class="text-[11px] text-slate-300 mt-1 line-clamp-2 leading-relaxed">${p.why_it_helps}</p>
        </div>
        <div class="text-[10px] text-indigo-300 font-medium pt-1 border-t border-slate-800/80">
          Deliverable: ${p.deliverable}
        </div>
      </div>
    `).join('');
  }

  initLucide();
}

// ----------------- Radar Chart ----------------- //

function renderRadarChart(canvasId, radarData) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !radarData) return;

  if (state.radarChartInstance) {
    state.radarChartInstance.destroy();
  }

  const ctx = canvas.getContext('2d');
  state.radarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: radarData.categories || ['Languages', 'Frameworks', 'Databases', 'Cloud', 'System Design', 'CS Fundamentals'],
      datasets: [
        {
          label: 'Current Digital Twin',
          data: radarData.student_scores || [0, 0, 0, 0, 0, 0],
          backgroundColor: 'rgba(99, 102, 241, 0.25)',
          borderColor: '#818cf8',
          borderWidth: 2,
          pointBackgroundColor: '#6366f1',
          pointBorderColor: '#fff',
        },
        {
          label: 'Industry Benchmark',
          data: radarData.benchmark_scores || [90, 85, 80, 75, 80, 85],
          backgroundColor: 'rgba(6, 182, 212, 0.15)',
          borderColor: '#22d3ee',
          borderWidth: 2,
          borderDash: [4, 4],
          pointBackgroundColor: '#06b6d4',
          pointBorderColor: '#fff',
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          pointLabels: {
            color: '#94a3b8',
            font: { size: 10, family: 'Plus Jakarta Sans', weight: '600' }
          },
          ticks: { display: false, min: 0, max: 100 }
        }
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#cbd5e1', font: { family: 'Plus Jakarta Sans', size: 11 } }
        }
      }
    }
  });
}

// ----------------- Detailed Roadmap View ----------------- //

function renderRoadmapView() {
  if (!state.orchestrationData) return;
  const roadmap = state.orchestrationData.roadmap_output;

  const titleEl = document.getElementById('roadmapRoleTitle');
  if (titleEl) titleEl.textContent = `${roadmap.target_role} 5-Phase Upskilling Roadmap`;

  const timeEl = document.getElementById('roadmapTimelineBadge');
  if (timeEl) timeEl.textContent = roadmap.estimated_timeline;

  const container = document.getElementById('roadmapPhasesContainer');
  if (!container) return;

  container.innerHTML = roadmap.phases.map((phase) => `
    <div class="glass-panel p-6 rounded-2xl space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-3">
          <div class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-xs font-bold text-white">
            0${phase.phase_number}
          </div>
          <h3 class="text-base font-bold text-white">${phase.phase_name}</h3>
        </div>
        <span class="text-xs px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-semibold">${phase.timeframe}</span>
      </div>

      <div class="space-y-1 pt-1">
        <span class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider block">Key Competencies to Master:</span>
        <div class="flex flex-wrap gap-1.5">
          ${phase.skills_to_learn.map(s => `
            <span class="text-xs px-2.5 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-slate-200">${s}</span>
          `).join('')}
        </div>
      </div>

      <div class="space-y-1 pt-1">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">Suggested Practical Activities:</span>
        <ul class="text-xs text-slate-300 space-y-1">
          ${phase.suggested_activities.map(act => `
            <li class="flex items-start gap-2">
              <span class="text-indigo-400 font-bold">➔</span>
              <span>${act}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/20 flex items-start gap-2 text-xs text-emerald-300">
        <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
        <div>
          <strong class="text-emerald-400 font-semibold">Expected Phase Outcome:</strong>
          <p class="text-slate-200 mt-0.5">${phase.expected_outcome}</p>
        </div>
      </div>
    </div>
  `).join('');

  initLucide();
}

// ----------------- Detailed Projects View ----------------- //

function renderProjectsView() {
  if (!state.orchestrationData) return;
  const projectData = state.orchestrationData.project_output;

  const headingEl = document.getElementById('projectsRoleHeading');
  if (headingEl) headingEl.textContent = `Recommended Portfolio Blueprints for ${projectData.target_role}`;

  const container = document.getElementById('projectCardsContainer');
  if (container) {
    container.innerHTML = projectData.recommended_projects.map(p => `
      <div class="glass-panel p-6 rounded-2xl glass-panel-hover flex flex-col justify-between space-y-4">
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-bold">${p.difficulty}</span>
            <span class="text-xs text-slate-400">Flagship Portfolio</span>
          </div>
          <h3 class="text-lg font-bold text-white">${p.title}</h3>
          
          <div class="mt-3 p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300">
            <strong class="text-indigo-300 block mb-1">Architecture Overview:</strong>
            <p class="text-slate-300 leading-relaxed font-mono text-[11px]">${p.architecture_overview}</p>
          </div>

          <div class="mt-3 space-y-1">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">Why This Project Matters:</span>
            <p class="text-xs text-slate-300 leading-relaxed">${p.why_it_helps}</p>
          </div>
        </div>

        <div>
          <div class="border-t border-slate-800 pt-3 flex flex-wrap gap-1.5">
            ${p.skills_gained.map(s => `
              <span class="text-[10px] px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-500/30 font-medium">${s}</span>
            `).join('')}
          </div>
          <div class="mt-2 text-[11px] text-slate-400 flex items-center gap-1">
            <i data-lucide="box" class="w-3.5 h-3.5 text-cyan-400"></i> Deliverable: ${p.deliverable}
          </div>
        </div>
      </div>
    `).join('');
  }

  const tipsEl = document.getElementById('portfolioTipsList');
  if (tipsEl && projectData.portfolio_activities) {
    tipsEl.innerHTML = projectData.portfolio_activities.map(t => `
      <li class="flex items-start gap-2 text-xs text-slate-300">
        <i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
        <span>${t}</span>
      </li>
    `).join('');
  }

  initLucide();
}

// ----------------- Future Career Simulation ----------------- //

function renderSimulationView() {
  if (!state.orchestrationData) return;
  const sim = state.orchestrationData.simulation_output;

  const curTitleEl = document.getElementById('simCurrentTitle');
  if (curTitleEl) curTitleEl.textContent = sim.current_twin.title;

  const curScoreEl = document.getElementById('simCurrentScore');
  if (curScoreEl) curScoreEl.textContent = `${Math.round(sim.current_twin.readiness_score || 0)}%`;

  const curTierEl = document.getElementById('simCurrentTier');
  if (curTierEl) curTierEl.textContent = sim.current_twin.competitive_tier;

  const curStrEl = document.getElementById('simCurrentStrengths');
  if (curStrEl) curStrEl.textContent = sim.current_twin.strengths_highlight;

  const futTitleEl = document.getElementById('simFutureTitle');
  if (futTitleEl) futTitleEl.textContent = sim.future_simulated_twin.title;

  const futScoreEl = document.getElementById('simFutureScore');
  if (futScoreEl) futScoreEl.textContent = `${Math.round(sim.future_simulated_twin.readiness_score || 0)}%`;

  const futTierEl = document.getElementById('simFutureTier');
  if (futTierEl) futTierEl.textContent = sim.future_simulated_twin.competitive_tier;

  const futStrEl = document.getElementById('simFutureStrengths');
  if (futStrEl) futStrEl.textContent = sim.future_simulated_twin.strengths_highlight;

  const boostBadgeEl = document.getElementById('simScoreBoostBadge');
  if (boostBadgeEl) boostBadgeEl.textContent = `+${Math.round(sim.score_improvement || 0)}% Estimated Gain`;

  const verdictEl = document.getElementById('simVerdictText');
  if (verdictEl) verdictEl.textContent = sim.simulation_verdict;

  const disclaimerEl = document.getElementById('simDisclaimerText');
  if (disclaimerEl) disclaimerEl.textContent = sim.disclaimer;

  const closedEl = document.getElementById('simGapsClosedList');
  if (closedEl) {
    closedEl.innerHTML = sim.gaps_closed.map(g => `
      <span class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1.5">
        <i data-lucide="check-check" class="w-3.5 h-3.5 text-emerald-400"></i> Closed: ${g}
      </span>
    `).join('');
  }

  const unlockedEl = document.getElementById('simUnlockedCapabilitiesList');
  if (unlockedEl) {
    unlockedEl.innerHTML = sim.new_capabilities_unlocked.map(u => `
      <li class="flex items-start gap-2 text-xs text-slate-200">
        <span class="text-cyan-400 font-bold">⚡</span>
        <span>${u}</span>
      </li>
    `).join('');
  }

  initLucide();
}

async function runCustomSimulation() {
  const checkboxes = document.querySelectorAll('.sim-action-checkbox:checked');
  const actions = Array.from(checkboxes).map(c => c.value);

  if (actions.length === 0) {
    showToast('Please select at least one action to simulate', 'error');
    return;
  }

  showLoader(true, "Simulating future career trajectory...");
  try {
    const res = await fetch(`${API_BASE}/twin/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        actions: actions,
        custom_scenario: ""
      })
    });
    if (res.ok) {
      const result = await res.json();
      state.orchestrationData.simulation_output = result;
      renderSimulationView();
      if (window.confetti) {
        window.confetti({ particleCount: 30, spread: 60, origin: { y: 0.7 } });
      }
      showToast('Future Twin simulation updated!', 'success');
    }
  } catch (err) {
    showToast('Failed to run simulation', 'error');
  } finally {
    showLoader(false);
  }
}

// ----------------- Strategy Master Report ----------------- //

function renderStrategyReport() {
  if (!state.orchestrationData || !state.profile) return;
  const strat = state.orchestrationData.strategist_output;
  const prof = state.profile;

  const candidateDisplay = prof.name && prof.name.trim() ? prof.name.trim() : "Your Career Twin";
  const nameEl = document.getElementById('stratReportCandidateName');
  if (nameEl) nameEl.textContent = candidateDisplay;

  const roleEl = document.getElementById('stratReportTargetRole');
  if (roleEl) roleEl.textContent = prof.target_career || "Software Engineer";

  const assessEl = document.getElementById('stratAssessmentText');
  if (assessEl) assessEl.textContent = strat.current_career_assessment;

  const stepsEl = document.getElementById('stratImmediateStepsList');
  if (stepsEl) {
    stepsEl.innerHTML = strat.immediate_next_steps.map((step, idx) => `
      <div class="p-3.5 rounded-xl bg-slate-900/70 border border-slate-800 flex items-start gap-3">
        <div class="w-6 h-6 rounded-lg bg-indigo-600/30 text-indigo-400 font-bold text-xs flex items-center justify-center shrink-0">
          ${idx + 1}
        </div>
        <p class="text-xs text-slate-200 leading-relaxed">${step}</p>
      </div>
    `).join('');
  }

  const shortEl = document.getElementById('stratShortTermList');
  if (shortEl) {
    shortEl.innerHTML = strat.short_term_strategy.map(item => `
      <li class="flex items-start gap-2 text-xs text-slate-300">
        <span class="text-cyan-400 font-bold">➔</span>
        <span>${item}</span>
      </li>
    `).join('');
  }

  const longEl = document.getElementById('stratLongTermList');
  if (longEl) {
    longEl.innerHTML = strat.long_term_strategy.map(item => `
      <li class="flex items-start gap-2 text-xs text-slate-300">
        <span class="text-emerald-400 font-bold">➔</span>
        <span>${item}</span>
      </li>
    `).join('');
  }

  const matrixEl = document.getElementById('stratPriorityMatrixContainer');
  if (matrixEl && strat.action_priority_matrix) {
    matrixEl.innerHTML = Object.entries(strat.action_priority_matrix).map(([phase, action]) => `
      <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
        <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider block mb-1">${phase}</span>
        <p class="text-xs text-slate-200">${action}</p>
      </div>
    `).join('');
  }

  initLucide();
}

function printStrategyReport() {
  window.print();
}

// ----------------- Profile Studio ----------------- //

function populateProfileForm() {
  if (!state.profile) return;
  const p = state.profile;

  const nameInput = document.getElementById('profName');
  if (nameInput) nameInput.value = p.name || '';

  const degreeInput = document.getElementById('profDegree');
  if (degreeInput) degreeInput.value = p.degree || 'B.Tech';

  const branchInput = document.getElementById('profBranch');
  if (branchInput) branchInput.value = p.branch || 'Computer Science Engineering';

  const yearInput = document.getElementById('profYear');
  if (yearInput) yearInput.value = p.year_of_study || '3rd Year';

  const cgpaInput = document.getElementById('profCgpa');
  if (cgpaInput) cgpaInput.value = p.cgpa !== null && p.cgpa !== undefined ? p.cgpa : '';

  const skillsInput = document.getElementById('profSkills');
  if (skillsInput) skillsInput.value = (p.current_skills || []).join(', ');

  const projInput = document.getElementById('profProjects');
  if (projInput) projInput.value = (p.projects || []).join('\n');

  const certInput = document.getElementById('profCerts');
  if (certInput) certInput.value = (p.certifications || []).join('\n');

  const jdInput = document.getElementById('profJobDescription');
  if (jdInput) jdInput.value = p.job_description || '';

  const intInput = document.getElementById('profInterests');
  if (intInput) intInput.value = (p.career_interests || []).join(', ');

  const targetInput = document.getElementById('profTargetCareer');
  if (targetInput) targetInput.value = p.target_career || 'Software Engineer';

  const dreamInput = document.getElementById('profDreamCompany');
  if (dreamInput) dreamInput.value = p.dream_company || '';
}

async function saveProfileFromForm(e) {
  if (e) e.preventDefault();
  showLoader(true, "Saving profile & updating Digital Twin...");

  const updated = {
    ...state.profile,
    name: document.getElementById('profName')?.value.trim() || '',
    degree: document.getElementById('profDegree')?.value.trim() || 'B.Tech',
    branch: document.getElementById('profBranch')?.value.trim() || 'Computer Science Engineering',
    year_of_study: document.getElementById('profYear')?.value.trim() || '3rd Year',
    cgpa: parseFloat(document.getElementById('profCgpa')?.value) || null,
    current_skills: parseCommaList(document.getElementById('profSkills')?.value),
    projects: parseNewlineList(document.getElementById('profProjects')?.value),
    certifications: parseNewlineList(document.getElementById('profCerts')?.value),
    job_description: document.getElementById('profJobDescription')?.value.trim() || '',
    career_interests: parseCommaList(document.getElementById('profInterests')?.value),
    target_career: document.getElementById('profTargetCareer')?.value.trim() || 'Software Engineer',
    dream_company: document.getElementById('profDreamCompany')?.value.trim() || ''
  };

  try {
    const res = await fetch(`${API_BASE}/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updated)
    });
    if (res.ok) {
      state.profile = await res.json();
      showToast('Profile updated & Digital Twin synchronized!', 'success');
      await refreshAll();
      switchTab('dashboard');
    }
  } catch (err) {
    showToast('Failed to save profile', 'error');
  } finally {
    showLoader(false);
  }
}

async function loadSampleProfile(sampleId) {
  showLoader(true, "Loading demonstration profile...");
  try {
    const res = await fetch(`${API_BASE}/profile/sample/${sampleId}`, { method: 'POST' });
    if (res.ok) {
      state.profile = await res.json();
      sessionStorage.setItem('active_session_upload', 'Demo Profile Loaded');
      showToast(`Loaded Demonstration Profile (${state.profile.target_career})`, 'success');
      await refreshAll();
      switchTab('dashboard');
    }
  } catch (err) {
    showToast('Failed to load sample profile', 'error');
  } finally {
    showLoader(false);
  }
}

// ----------------- Helpers & Event Listeners ----------------- //

function parseCommaList(str) {
  return (str || '').split(',').map(s => s.trim()).filter(s => s.length > 0);
}

function parseNewlineList(str) {
  return (str || '').split('\n').map(s => s.trim()).filter(s => s.length > 0);
}

function showLoader(visible, text = "Evaluating skills & calculating deterministic readiness score...") {
  const loader = document.getElementById('globalLoader');
  const loaderText = document.getElementById('globalLoaderText');
  if (loaderText) loaderText.textContent = text;
  if (loader) loader.classList.toggle('hidden', !visible);
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  const bg = type === 'success' ? 'bg-emerald-600' : type === 'error' ? 'bg-rose-600' : 'bg-indigo-600';
  toast.className = `${bg} text-white text-xs font-semibold px-4 py-3 rounded-xl shadow-2xl flex items-center gap-2 transform transition-all duration-300 translate-y-2 opacity-0`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 350);
  }, 3500);
}

function setupEventListeners() {
  const profileForm = document.getElementById('profileForm');
  if (profileForm) {
    profileForm.addEventListener('submit', saveProfileFromForm);
  }

  const fileInput = document.getElementById('resumeFileInput');
  if (fileInput) {
    fileInput.addEventListener('change', handleResumeFileUpload);
  }

  const roleSelect = document.getElementById('quickTargetRoleSelect');
  if (roleSelect) {
    roleSelect.addEventListener('change', (e) => {
      handleTargetRoleSelectChange(e.target.value);
    });
  }

  const customInput = document.getElementById('quickCustomRoleInput');
  if (customInput) {
    customInput.addEventListener('input', (e) => {
      const val = e.target.value.trim() || "Custom Role";
      const roleEl = document.getElementById('headerTargetRole');
      const targetGoalEl = document.getElementById('dashTargetGoal');
      if (roleEl) roleEl.textContent = val;
      if (targetGoalEl) targetGoalEl.textContent = val;
    });
  }
}
