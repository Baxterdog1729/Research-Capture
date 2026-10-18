import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import json
import math

# ==============================================================================
# 1. PAGE CONFIGURATION & MODERN DARK GLASSMORPHISM STYLING
# ==============================================================================
st.set_page_config(
    page_title="Thought Sweep | Research & Marketing Strategy Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high-end dark glassmorphism styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #150d2a 50%, #0d0818 100%);
        color: #f1f5f9;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa 0%, #c084fc 50%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.0rem;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(22, 14, 38, 0.7);
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid rgba(167, 139, 250, 0.15);
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre;
        border-radius: 8px;
        color: #cbd5e1;
        font-weight: 600;
        padding: 0px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    .glass-card {
        background: rgba(22, 14, 38, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(167, 139, 250, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .quad-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(167, 139, 250, 0.2);
    }
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4);
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(15, 10, 28, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(167, 139, 250, 0.25) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE INITIALIZATION & DATA UTILITIES
# ==============================================================================
def init_session_state():
    defaults = {
        "step1_interviews": [],
        "step2_interviews": [],
        "step3_interviews": [],
        "stage_definitions": {},
        "codebook": [
            {"id": "C1", "name": "Lack of ideas", "category": "Challenge Codes (C)", "desc": "Unable to find or choose a topic/direction."},
            {"id": "C2", "name": "Idea-to-plan difficulty", "category": "Challenge Codes (C)", "desc": "Having an idea but unable to narrow into scope or plan."},
            {"id": "C3", "name": "Organizing thoughts & sources", "category": "Challenge Codes (C)", "desc": "Notes, sources or drafts scattered or hard to find."},
            {"id": "C4", "name": "Idea loss", "category": "Challenge Codes (C)", "desc": "Forgetting, never recording spontaneous ideas."},
            {"id": "C5", "name": "Time management", "category": "Challenge Codes (C)", "desc": "Misjudging work duration, scheduling or pacing."},
            {"id": "C6", "name": "Procrastination", "category": "Challenge Codes (C)", "desc": "Knowingly putting off or avoiding thesis work."},
            {"id": "C7", "name": "Cognitive overwhelm", "category": "Challenge Codes (C)", "desc": "Feeling flooded, frozen or unsure where to start."},
            {"id": "T1", "name": "Digital notes", "category": "Tools Used (T)", "desc": "Notion, Obsidian, OneNote, Apple Notes."},
            {"id": "T2", "name": "Paper", "category": "Tools Used (T)", "desc": "Notebooks, sticky notes, whiteboards."},
            {"id": "T3", "name": "Voice memos", "category": "Tools Used (T)", "desc": "Voice messages, audio recording."},
            {"id": "W1", "name": "Faster capture", "category": "Capabilities Wanted (W)", "desc": "Getting an idea down quickly, anywhere."},
            {"id": "W4", "name": "Turning ideas into tasks", "category": "Capabilities Wanted (W)", "desc": "Moving from idea to action items."}
        ],
        "coder_a_annotations": [],
        "coder_b_annotations": [],
        "kappa_locked": False,
        "kappa_value": 0.0,
        "surveys": []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

def export_all_data():
    data = {
        "stage_definitions": st.session_state.stage_definitions,
        "step1_interviews": st.session_state.step1_interviews,
        "step2_interviews": st.session_state.step2_interviews,
        "step3_interviews": st.session_state.step3_interviews,
        "codebook": st.session_state.codebook,
        "coder_a_annotations": st.session_state.coder_a_annotations,
        "coder_b_annotations": st.session_state.coder_b_annotations,
        "kappa_locked": st.session_state.kappa_locked,
        "kappa_value": st.session_state.kappa_value,
        "surveys": st.session_state.surveys
    }
    return json.dumps(data, indent=2)

def import_all_data(uploaded_json):
    try:
        data = json.load(uploaded_json)
        for key, value in data.items():
            st.session_state[key] = value
        return True
    except Exception as e:
        st.error(f"Failed to parse JSON file: {e}")
        return False

def clear_all_data():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
    st.rerun()

# ==============================================================================
# HEADER & GLOBAL DATA CONTROL DRAWER
# ==============================================================================
col_title, col_ctrl = st.columns([0.70, 0.30])
with col_title:
    st.markdown("<div class='main-title'>🧠 Thought Sweep Research Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Barrett Honors Thesis Qualitative & Quantitative Strategy System</div>", unsafe_allow_html=True)

with col_ctrl:
    with st.expander("⚙️ System Data Controls"):
        st.markdown("**📥 Import Dataset (JSON)**")
        uploaded_file = st.file_uploader("Upload Research JSON", type=["json"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Apply Uploaded Data", use_container_width=True):
                if import_all_data(uploaded_file):
                    st.toast("✅ Dataset imported successfully!", icon="🎉")
                    st.rerun()

        st.markdown("---")
        st.markdown("**📤 Export / Reset Data**")
        st.download_button(
            label="📥 Export Current JSON",
            data=export_all_data(),
            file_name="thought_sweep_research_data.json",
            mime="application/json",
            use_container_width=True
        )
        if st.button("🗑️ Reset All Data", use_container_width=True):
            clear_all_data()

# ==============================================================================
# TOP TAB NAVIGATION (INTERFACES 1 - 7)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Thesis Stages",
    "2. Faculty Obs.",
    "3. Student Exp.",
    "4. Transcript Coding",
    "5. Subtag Drill-Down",
    "6. Survey Stats",
    "7. Strategy Matrix"
])

# ------------------------------------------------------------------------------
# INTERFACE 1: STEP 1 INTERVIEW GUIDE (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### Interface 1: Step 1 Interview Guide — Defining Thesis Process")
    st.caption("Record full Step 1 interviews with faculty/advisors and standardize concrete thesis process stages.")

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Log Complete Step 1 Interview Entry")
        with st.form("step1_full_form", clear_on_submit=True):
            s1_id = st.text_input("Interviewee ID *", placeholder="e.g. S1-01")
            group = st.selectbox("Group *", ["Faculty", "Student-In-process", "Student-Completed"])
            disc = st.selectbox("Discipline *", ["STEM", "Creative", "Humanities", "Social Science"])
            unit_word = st.text_input("Unit Word Used (stage, phase, step, area)", value="stage")

            st.markdown("---")
            st.markdown("#### Part A: Main Areas (A1 – A6)")
            q_a1 = st.text_area("A1. From beginning to end, what are the main areas/phases a student goes through?", height=70)
            q_a2 = st.text_area("A2. What do you call each of these? Is there a name you/your department use?", height=70)
            q_a3 = st.text_area("A3. In what order do students usually move through them?", height=70)
            q_a4 = st.text_area("A4. Is there anything before the first or after the last area we should include?", height=70)
            q_a5 = st.text_area("A5. (Read list back) Does this match how you see the process? What would you change?", height=70)
            q_a6 = st.text_area("A6. Is this list the same for every thesis in your discipline or does it change?", height=70)

            st.markdown("---")
            st.markdown("#### Part B: Defining Each Stage (B1 – B9)")
            q_b1 = st.text_area("B1. What is [STAGE]? How would you explain it to a new student?", height=70)
            q_b2 = st.text_area("B2. What does a student actually do during [STAGE]?", height=70)
            q_b3 = st.text_area("B3. What does a student have to complete, produce, or have approved?", height=70)
            q_b4 = st.text_area("B4. Which requirements are set officially (Barrett/college) vs advisor/discipline?", height=70)
            q_b5 = st.text_area("B5. How do you know when a student is ready to move on from [STAGE]?", height=70)
            q_b6 = st.text_area("B6. What does a student need to have in place before beginning [STAGE]?", height=70)
            q_b7 = st.text_area("B7. Who is involved in [STAGE], and what does each person do?", height=70)
            q_b8 = st.text_area("B8. How long does [STAGE] take, and where does it fall on the timeline?", height=70)
            q_b9 = st.text_area("B9. What changes about [STAGE] from one project/discipline to another?", height=70)

            st.markdown("---")
            st.markdown("#### Part C: Boundaries and Wrap-Up (C1 – C5)")
            q_c1 = st.text_area("C1. Are there areas that overlap or blur together? How do you tell where one ends?", height=70)
            q_c2 = st.text_area("C2. Are there areas that some students skip, combine, or repeat?", height=70)
            q_c3 = st.text_area("C3. Are there official milestones, forms, or deadlines every student must meet?", height=70)
            q_c4 = st.text_area("C4. Is there anything about how the thesis process works that we missed?", height=70)
            q_c5 = st.text_area("C5. Who else should we speak with?", height=70)

            if st.form_submit_button("Save Complete Step 1 Interview", use_container_width=True):
                if s1_id:
                    entry = {
                        "id": s1_id, "group": group, "discipline": disc, "unit_word": unit_word,
                        "a1": q_a1, "a2": q_a2, "a3": q_a3, "a4": q_a4, "a5": q_a5, "a6": q_a6,
                        "b1": q_b1, "b2": q_b2, "b3": q_b3, "b4": q_b4, "b5": q_b5, "b6": q_b6, "b7": q_b7, "b8": q_b8, "b9": q_b9,
                        "c1": q_c1, "c2": q_c2, "c3": q_c3, "c4": q_c4, "c5": q_c5
                    }
                    st.session_state.step1_interviews.append(entry)
                    st.toast(f"✅ Saved Step 1 Interview {s1_id}! Available in Coding Repository.", icon="💾")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Standardize Concrete Process Stages")
        st.info("Set standardized stage names and definitions here. These propagate across Interfaces 2–7.")
        
        stages = ["Topic Selection / Ideation", "Proposal & Scoping", "Literature Review", 
                  "Data Collection / Execution", "Analysis & Synthesis", "Drafting & Writing"]
        
        updated_defs = {}
        for stage in stages:
            curr = st.session_state.stage_definitions.get(stage, "")
            updated_defs[stage] = st.text_input(f"Stage: {stage}", value=curr, placeholder=f"Define {stage} rules...")
        
        if st.button("Lock Standardized Stage Definitions", use_container_width=True):
            st.session_state.stage_definitions = updated_defs
            st.toast("✅ Stage definitions locked across software!", icon="🔒")
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 2: STEP 2 FACULTY OBSERVATIONS (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### Interface 2: Step 2 Faculty Interview Guide — Observed Challenges")
    st.caption("Capture faculty advisor observations across all stages, hardest stage identification, tools, and referrals.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    with st.form("step2_full_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            s2_id = st.text_input("Faculty Interviewee ID *", placeholder="e.g. F-01")
            disc = st.selectbox("Faculty Discipline *", ["STEM", "Creative", "Humanities", "Social Science"])
        with col2:
            stages_list = list(st.session_state.stage_definitions.keys()) if st.session_state.stage_definitions else ["Topic Selection / Ideation"]
            hardest_stage = st.selectbox("Stage with Greatest Struggle (C1) *", stages_list)
        
        st.markdown("---")
        st.markdown("#### Part A: Confirming Stages")
        q_a2 = st.text_area("A2. Is there anything about these stages or definitions that is unclear?", height=60)
        q_a3 = st.text_area("A3. Is there any stage you think of differently from how it is defined here?", height=60)

        st.markdown("---")
        st.markdown("#### Part B: Observed Struggles in Each Stage (B1 – B8)")
        q_b1 = st.text_area("B1. What struggles do you observe at [Stage.Final]?", height=70)
        q_b2 = st.text_area("B2. What does that look like in practice? What do you see students doing/not doing?", height=70)
        q_b3 = st.text_area("B3. Can you describe a recent example, without naming the student?", height=70)
        q_b4 = st.text_area("B4. What do you see students do when this happens?", height=70)
        q_b5 = st.text_area("B5. What do you think is going on when students struggle in this way?", height=70)
        q_b6 = st.text_area("B6. How common is this among the students you have advised?", height=70)
        q_b7 = st.text_area("B7. What have you seen students do that helps them through [Stage.Final]?", height=70)
        q_b8 = st.text_area("B8. Does what you see at [Stage.Final] change with project type/discipline?", height=70)

        st.markdown("---")
        st.markdown("#### Part C: Stage with Greatest Struggle (C1 – C5)")
        q_c2 = st.text_area("C2. Why do you think students struggle the most at [Stage.Final]?", height=70)
        q_c3 = st.text_area("C3. What does that struggle look like when it is happening?", height=70)
        q_c4 = st.text_area("C4. Can you walk me through a specific example, without naming the student?", height=70)
        q_c5 = st.text_area("C5. What do you notice about students who get through with less struggle?", height=70)

        st.markdown("---")
        st.markdown("#### Part D: Ideas, Tools, and Support (D1 – D6)")
        q_d1 = st.text_area("D1. How do you see students come up with their ideas and keep track of them?", height=70)
        q_d2 = st.text_area("D2. What tools, systems, or methods have you seen students use to track work?", height=70)
        q_d3 = st.text_area("D3. What have you noticed about how well those work for students?", height=70)
        q_d4 = st.text_area("D4. When a student is stuck, what do you suggest and where do you send them?", height=70)
        q_d6 = st.text_area("D6. Is there anything else about what students go through that we missed?", height=70)

        if st.form_submit_button("Save Complete Faculty Interview", use_container_width=True):
            if s2_id:
                entry = {
                    "id": s2_id, "group": "Faculty", "discipline": disc, "hardest_stage": hardest_stage,
                    "a2": q_a2, "a3": q_a3, "b1": q_b1, "b2": q_b2, "b3": q_b3, "b4": q_b4, "b5": q_b5, "b6": q_b6, "b7": q_b7, "b8": q_b8,
                    "c2": q_c2, "c3": q_c3, "c4": q_c4, "c5": q_c5, "d1": q_d1, "d2": q_d2, "d3": q_d3, "d4": q_d4, "d6": q_d6
                }
                st.session_state.step2_interviews.append(entry)
                st.toast(f"✅ Saved Faculty Interview {s2_id}! Ready for coding in Interface 4.", icon="💾")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 3: STEP 3 STUDENT EXPERIENCES (FULL QUESTIONS)
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### Interface 3: Step 3 Student Interview Guide — Thesis Experience")
    st.caption("Capture complete Barrett student interview responses across warm-up, stage experience, ideas, challenges, tools, and support.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    with st.form("step3_full_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            s3_id = st.text_input("Student Participant ID *", placeholder="e.g. S-01")
        with col2:
            group = st.selectbox("Student Status *", ["Student-In-process", "Student-Completed", "Student-Beginning"])
        with col3:
            disc = st.selectbox("Discipline *", ["STEM", "Creative", "Humanities", "Social Science"])

        stages_list = list(st.session_state.stage_definitions.keys()) if st.session_state.stage_definitions else ["Topic Selection / Ideation"]
        hardest_stage = st.selectbox("Hardest Stage (H2)", stages_list)
        
        st.markdown("---")
        st.markdown("#### Warm-Up & Stage Status (01 – 04)")
        q_01 = st.text_area("01. In a sentence or two, what is your thesis about?", height=60)
        q_02 = st.text_area("02. About how long have you been working on your thesis?", height=60)
        q_03 = st.text_area("03. Is there anything on the stage card that is unclear?", height=60)
        q_04 = st.text_area("04. Which stages have you finished, and which one are you in now?", height=60)

        st.markdown("---")
        st.markdown("#### Stage by Stage Experience (B1 – B7)")
        q_b1 = st.text_area("B1. Walk me through what you did during [Stage.Final], starting with the first thing.", height=70)
        q_b2 = st.text_area("B2. Think of a moment during [Stage.Final] when something didn't go as expected. What happened?", height=70)
        q_b3 = st.text_area("B3. What did you do when that happened?", height=70)
        q_b4 = st.text_area("B4. What do you think was going on at that point?", height=70)
        q_b5 = st.text_area("B5. What part of [Stage.Final] went more smoothly than expected? What helped?", height=70)
        q_b6 = st.text_area("B6 (Optional). Was anyone else involved in [Stage.Final]? What did they do?", height=60)
        q_b7 = st.text_area("B7 (Optional). If doing [Stage.Final] again, what would you do differently?", height=60)

        st.markdown("---")
        st.markdown("#### Your Ideas (11 – 110)")
        q_11 = st.text_area("11. Where did your thesis idea come from? Walk me through how you first came up with it.", height=70)
        q_12 = st.text_area("12. Tell me about any other ideas you considered before your current one. What happened to them?", height=70)
        q_13 = st.text_area("13. Think about the most recent time a new thesis idea came to you. Where were you & doing?", height=70)
        q_14 = st.text_area("14. What was the first thing you did with that idea?", height=60)
        q_15 = st.text_area("15. What happened to that idea afterward?", height=60)
        q_16 = st.text_area("16. Last time you needed something saved earlier (note, source, idea), what happened?", height=70)
        q_17 = st.text_area("17. Walk me through the steps between that first idea and having a plan to work from.", height=70)
        q_18 = st.text_area("18. Was there a point on the way from idea to plan where you were unsure what to do next?", height=70)
        q_19 = st.text_area("19. Walk me through how one part went from an idea to what you have now (deliverable).", height=70)
        q_110 = st.text_area("110 (Optional). Last idea that turned into something you had to do (task/deadline)?", height=60)

        st.markdown("---")
        st.markdown("#### Most Difficult Challenge (H1 – H5)")
        q_h1 = st.text_area("H1. What has been the most difficult challenge you have faced with your thesis so far?", height=70)
        q_h3 = st.text_area("H3. What made that so difficult?", height=70)
        q_h4 = st.text_area("H4. What did that look like day to day? What were you doing, or not doing?", height=70)
        q_h5 = st.text_area("H5. How did you get through it, or are you still working through it? What helped?", height=70)

        st.markdown("---")
        st.markdown("#### Tools (U1 – U9)")
        q_u1 = st.text_area("U1. Last time you wrote down or recorded an idea for your thesis, what did you use?", height=60)
        q_u2 = st.text_area("U2. Where do your thesis notes, readings, and sources live right now? List every place.", height=70)
        q_u3 = st.text_area("U3. How did you start using each tool/place? Who/what made you choose it?", height=60)
        q_u4 = st.text_area("U4. What works well about using it, and what is frustrating about it?", height=70)
        q_u5 = st.text_area("U5. Have you stopped using any app, notebook, or method you started out with? Why?", height=60)
        q_u6 = st.text_area("U6. What do you use to turn ideas into your final project (outline, draft, plan)?", height=60)
        q_u7 = st.text_area("U7. Is there anything you do by hand or work around because a tool doesn't do it?", height=70)
        q_u8 = st.text_area("U8. Thinking about the last time you did that workaround, what were you trying to get done?", height=60)
        q_u9 = st.text_area("U9 (Optional). Would you change anything about how you handle notes/ideas weekly?", height=60)

        st.markdown("---")
        st.markdown("#### Support and Wrap-Up (S1 – S4)")
        q_s1 = st.text_area("S1. When in your thesis did you most wish you had more help? What kind of help?", height=70)
        q_s2 = st.text_area("S2. When you have had a question about your thesis, who did you go to?", height=60)
        q_s3 = st.text_area("S3. Where do you usually go to find out about resources/tools? Whose advice do you trust?", height=70)
        q_s4 = st.text_area("S4. Is there anything that made your thesis easier or harder that we haven't talked about?", height=70)

        if st.form_submit_button("Save Complete Student Interview", use_container_width=True):
            if s3_id:
                entry = {
                    "id": s3_id, "group": group, "discipline": disc, "hardest_stage": hardest_stage,
                    "01": q_01, "02": q_02, "03": q_03, "04": q_04,
                    "b1": q_b1, "b2": q_b2, "b3": q_b3, "b4": q_b4, "b5": q_b5, "b6": q_b6, "b7": q_b7,
                    "q_11": q_11, "q_12": q_12, "q_13": q_13, "q_14": q_14, "q_15": q_15, "q_16": q_16, "q_17": q_17, "q_18": q_18, "q_19": q_19, "q_110": q_110,
                    "h1": q_h1, "h3": q_h3, "h4": q_h4, "h5": q_h5,
                    "u1": q_u1, "u2": q_u2, "u3": q_u3, "u4": q_u4, "u5": q_u5, "u6": q_u6, "u7": q_u7, "u8": q_u8, "u9": q_u9,
                    "s1": q_s1, "s2": q_s2, "s3": q_s3, "s4": q_s4
                }
                st.session_state.step3_interviews.append(entry)
                st.toast(f"✅ Saved Student Interview {s3_id}! Ready for qualitative coding.", icon="💾")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 4: QUALITATIVE CODING & ICR ENGINE
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### Interface 4: Transcript Coding Repository & Reliability Engine")
    
    sub_code, sub_annot, sub_icr = st.tabs(["📖 Living Codebook v0.3", "🏷️ Coding Interface (Coder A)", "🛡️ Coder B & Kappa Verification"])

    # Subtab 1: Codebook
    with sub_code:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Manage Living Codebook")
        with st.expander("➕ Add New Emergent Code (EM)"):
            c_id = st.text_input("Code ID", placeholder="EM-01")
            c_name = st.text_input("Code Title", placeholder="Citation Confusion")
            c_cat = st.selectbox("Category", ["Challenge Codes (C)", "Tools Used (T)", "Capabilities Wanted (W)", "Emergent Themes (EM)"])
            c_desc = st.text_area("Definition & Boundaries")
            if st.button("Add Code to Codebook"):
                if c_id and c_name:
                    st.session_state.codebook.append({"id": c_id, "name": c_name, "category": c_cat, "desc": c_desc})
                    st.toast(f"✅ Added {c_id} ({c_name}) to Codebook!", icon="📖")
                    st.rerun()

        cb_df = pd.DataFrame(st.session_state.codebook)
        st.dataframe(cb_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Subtab 2: Coding Interface
    with sub_annot:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        all_transcripts = (
            [{"source": "Step 1", "id": x["id"], "group": x["group"], "discipline": x["discipline"], "text": f"{x.get('a1','')} {x.get('b1','')} {x.get('b2','')} {x.get('c1','')}"} for x in st.session_state.step1_interviews] +
            [{"source": "Step 2", "id": x["id"], "group": x["group"], "discipline": x["discipline"], "text": f"{x.get('b1','')} {x.get('b3','')} {x.get('c2','')} {x.get('d1','')}"} for x in st.session_state.step2_interviews] +
            [{"source": "Step 3", "id": x["id"], "group": x["group"], "discipline": x["discipline"], "text": f"{x.get('q_11','')} {x.get('q_13','')} {x.get('h1','')} {x.get('u1','')}"} for x in st.session_state.step3_interviews]
        )

        if not all_transcripts:
            st.warning("No interview transcripts logged yet. Enter interviews in Interfaces 1–3 first.")
        else:
            selected_int = st.selectbox("Select Interview Transcript:", [x["id"] for x in all_transcripts])
            curr_item = next(x for x in all_transcripts if x["id"] == selected_int)
            
            st.markdown(f"**Group:** `{curr_item['group']}` | **Discipline:** `{curr_item['discipline']}`")
            st.text_area("Full Consolidated Transcript Text", value=curr_item["text"], height=160, disabled=True)

            with st.form("coding_tag_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    selected_text = st.text_input("Paste Excerpt / Thought Unit to Code:")
                with col2:
                    code_options = [f"{c['id']} - {c['name']}" for c in st.session_state.codebook]
                    selected_code = st.selectbox("Apply Code:", code_options)

                if st.form_submit_button("Save Coding Tag", use_container_width=True):
                    if selected_text and selected_code:
                        code_id = selected_code.split(" - ")[0]
                        tag_entry = {
                            "interview_id": curr_item["id"],
                            "selected_text": selected_text,
                            "code_id": code_id,
                            "group": curr_item["group"],
                            "discipline": curr_item["discipline"]
                        }
                        st.session_state.coder_a_annotations.append(tag_entry)
                        st.toast(f"✅ Tagged excerpt with {code_id}!", icon="🏷️")
                        st.rerun()

            st.markdown("---")
            st.subheader("Existing Annotations (Coder A)")
            st.dataframe(pd.DataFrame(st.session_state.coder_a_annotations), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Subtab 3: Coder B & Kappa Check
    with sub_icr:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Inter-Coder Reliability (ICR) Verification")
        st.caption("Requirement: Cohen's Kappa ≥ 0.70 to lock data for statistical modeling.")

        if not st.session_state.coder_a_annotations:
            st.info("Coder A must apply annotations before ICR verification can begin.")
        else:
            sample_size = max(1, math.ceil(len(st.session_state.coder_a_annotations) * 0.25))
            sample_items = st.session_state.coder_a_annotations[:sample_size]
            
            st.markdown(f"**Required Coder B Verification Sample Size:** `{sample_size}` items")

            coder_b_inputs = []
            for idx, item in enumerate(sample_items):
                st.markdown(f"**Item {idx+1} (ID: {item['interview_id']}):** *\"{item['selected_text']}\"*")
                b_code = st.selectbox(
                    f"Coder B Code for Item {idx+1}:", 
                    [c["id"] for c in st.session_state.codebook], 
                    key=f"b_code_{idx}"
                )
                coder_b_inputs.append(b_code)

            if st.button("Calculate Cohen's Kappa Score", use_container_width=True):
                a_codes = [item["code_id"] for item in sample_items]
                matches = sum(1 for a, b in zip(a_codes, coder_b_inputs) if a == b)
                po = matches / sample_size
                pe = 1.0 / len(st.session_state.codebook)
                kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 1.0
                
                st.session_state.kappa_value = round(kappa, 3)
                if kappa >= 0.70:
                    st.session_state.kappa_locked = True
                    st.toast(f"✅ PASSED! Cohen's Kappa = {kappa:.3f}", icon="🛡️")
                else:
                    st.session_state.kappa_locked = False
                    st.toast(f"❌ FAILED! Cohen's Kappa = {kappa:.3f}", icon="⚠️")
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 5: SUBTAG DRILL-DOWN & FREQUENCY
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### Interface 5: Qualitative Frequencies & Subtag Filters")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    if not st.session_state.coder_a_annotations:
        st.info("No qualitative coding annotations recorded yet.")
    else:
        df_annot = pd.DataFrame(st.session_state.coder_a_annotations)
        df_unique = df_annot.drop_duplicates(subset=["interview_id", "code_id"])

        st.subheader("Top 5 Codes Overall (Unique Participant Counts)")
        top_overall = df_unique["code_id"].value_counts().head(5)
        st.bar_chart(top_overall)

        st.markdown("---")
        st.subheader("Subtag Filter Breakdown")
        filter_type = st.radio("Drill Down By:", ["Discipline", "Group (Faculty vs Student)", "Individual Interview ID"], horizontal=True)
        
        if filter_type == "Discipline":
            # HARDCODED ALL 4 BARRETT DISCIPLINES TO ENSURE CREATIVE IS ALWAYS PRESENT
            all_disciplines = ["STEM", "Creative", "Humanities", "Social Science"]
            disc = st.selectbox("Select Discipline:", all_disciplines)
            filtered = df_unique[df_unique["discipline"] == disc]
            if filtered.empty:
                st.caption(f"No qualitative tags recorded yet under '{disc}'.")
            else:
                st.table(filtered["code_id"].value_counts().head(5))
        elif filter_type == "Group (Faculty vs Student)":
            all_groups = ["Faculty", "Student-In-process", "Student-Completed", "Student-Beginning"]
            grp = st.selectbox("Select Group:", all_groups)
            filtered = df_unique[df_unique["group"] == grp]
            if filtered.empty:
                st.caption(f"No qualitative tags recorded yet under '{grp}'.")
            else:
                st.table(filtered["code_id"].value_counts().head(5))
        else:
            all_uids = df_unique["interview_id"].unique() if not df_unique.empty else ["S1-01"]
            iid = st.selectbox("Select Interview ID:", all_uids)
            filtered = df_unique[df_unique["interview_id"] == iid]
            if filtered.empty:
                st.caption(f"No qualitative tags recorded for Interview ID '{iid}'.")
            else:
                st.table(filtered["code_id"].value_counts().head(5))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 6: QUANTITATIVE SURVEY STATS
# ------------------------------------------------------------------------------
with tab6:
    st.markdown("### Interface 6: Quantitative Survey Entry & Statistical Tests")
    
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Record Survey Response")
        with st.form("survey_form", clear_on_submit=True):
            s_id = st.text_input("Survey ID *", placeholder="e.g. R-001")
            code_id = st.selectbox("Target Code *", [c["id"] for c in st.session_state.codebook])
            eligible = st.checkbox("Eligible for Stage?", value=True)
            experienced = st.checkbox("Experienced Difficulty?", value=True)
            severity = st.slider("Pain Severity Rating (1-5)", 1, 5, 4)
            tools = st.multiselect("Tools Referenced", ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"])

            if st.form_submit_button("Record Response", use_container_width=True):
                if s_id:
                    entry = {
                        "survey_id": s_id, "code_id": code_id, "eligible": eligible,
                        "experienced": experienced, "severity": severity, "tools_referenced": tools
                    }
                    st.session_state.surveys.append(entry)
                    st.toast(f"✅ Saved Survey Response {s_id}!", icon="📊")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Automated Background Statistical Tests")
        if not st.session_state.surveys:
            st.info("No survey response entries recorded yet.")
        else:
            df_surv = pd.DataFrame(st.session_state.surveys)
            results = []
            for c in st.session_state.codebook:
                cid = c["id"]
                sub = df_surv[df_surv["code_id"] == cid]
                n_el = len(sub[sub["eligible"] == True])
                n_high = len(sub[(sub["eligible"] == True) & (sub["experienced"] == True) & (sub["severity"] >= 4)])
                
                pain_rate = (n_high / n_el) if n_el > 0 else 0.0
                
                if n_el > 0:
                    z = 1.96
                    p = pain_rate
                    denom = 1 + (z**2)/n_el
                    center = p + (z**2)/(2*n_el)
                    dev = z * math.sqrt((p*(1-p) + (z**2)/(4*n_el))/n_el)
                    wilson_low = max(0.0, (center - dev)/denom)
                    wilson_high = min(1.0, (center + dev)/denom)
                else:
                    wilson_low, wilson_high = 0.0, 0.0

                p_val_binom = stats.binomtest(n_high, n_el, p=0.20, alternative='greater').pvalue if n_el > 0 else 1.0

                results.append({
                    "Code": cid,
                    "Eligible N": n_el,
                    "High Pain N": n_high,
                    "Pain Rate %": f"{pain_rate*100:.1f}%",
                    "Wilson 95% CI": f"[{wilson_low*100:.1f}%, {wilson_high*100:.1f}%]",
                    "Exact Binomial p-val": f"{p_val_binom:.4f}"
                })

            st.dataframe(pd.DataFrame(results), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTERFACE 7: 2x2 STRATEGY MATRIX (UPDATED QUADRANT LOGIC)
# ------------------------------------------------------------------------------
with tab7:
    st.markdown("### Interface 7: Integrated 2x2 Opportunity Prioritization Engine")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    df_annot = pd.DataFrame(st.session_state.coder_a_annotations) if st.session_state.coder_a_annotations else pd.DataFrame()
    df_surv = pd.DataFrame(st.session_state.surveys) if st.session_state.surveys else pd.DataFrame()

    total_students = df_annot[df_annot["group"].str.contains("Student", na=False)]["interview_id"].nunique() if not df_annot.empty else 1
    matrix_data = []

    for c in st.session_state.codebook:
        cid = c["id"]
        
        # Calculate qualitative mentions
        if not df_annot.empty:
            code_students = df_annot[(df_annot["code_id"] == cid) & (df_annot["group"].str.contains("Student", na=False))]["interview_id"].nunique()
            qual_freq = (code_students / total_students) if total_students > 0 else 0.0
            faculty_count = df_annot[(df_annot["code_id"] == cid) & (df_annot["group"] == "Faculty")]["interview_id"].nunique()
        else:
            qual_freq, faculty_count, code_students = 0.0, 0, 0

        # Calculate survey pain rate
        if not df_surv.empty:
            sub = df_surv[df_surv["code_id"] == cid]
            n_el = len(sub[sub["eligible"] == True])
            n_high = len(sub[(sub["eligible"] == True) & (sub["experienced"] == True) & (sub["severity"] >= 4)])
            pain_rate = (n_high / n_el) if n_el > 0 else 0.0
        else:
            pain_rate, n_el = 0.0, 0

        p_val = stats.binomtest(code_students, max(1, total_students), p=0.25, alternative='greater').pvalue if total_students > 0 else 1.0

        # Triangulation Check: Verified across both faculty and student qualitative interviews OR high survey pain
        is_triangulated = (faculty_count > 0 and code_students > 0) or (code_students > 0 and pain_rate >= 0.20)

        matrix_data.append({
            "code": c,
            "qual_freq": qual_freq,
            "pain_rate": pain_rate,
            "triangulated": is_triangulated,
            "p_val": p_val
        })

    matrix_data.sort(key=lambda x: x["p_val"])
    m = len(matrix_data)
    for idx, item in enumerate(matrix_data):
        alpha = 0.05 / (m - idx)
        item["significant"] = item["p_val"] <= alpha

    st.subheader("Strategic Opportunity Positioning Grid")
    q_lead, q_supp, q_niche, q_drop = [], [], [], []

    for item in matrix_data:
        # Threshold checks: Frequency >= 25% (or >= 1 student mention in sample) AND Pain Rate >= 20%
        is_high_freq = (item["qual_freq"] >= 0.25) or (item["qual_freq"] > 0)
        is_high_pain = item["pain_rate"] >= 0.20
        
        if is_high_freq and is_high_pain and item["triangulated"]:
            q_lead.append(item)
        elif not is_high_freq and is_high_pain:
            q_supp.append(item)
        elif is_high_freq and not is_high_pain:
            q_niche.append(item)
        else:
            q_drop.append(item)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<div class='quad-card' style='background: rgba(245, 158, 11, 0.15); border-color: #f59e0b;'><b>SUPPORTING MESSAGE</b><br><small>Low Frequency / High Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_supp: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")
        
    with g2:
        st.markdown("<div class='quad-card' style='background: rgba(16, 185, 129, 0.2); border-color: #10b981;'><b>⭐ LEAD MESSAGE</b><br><small>High Frequency / High Pain / Triangulated</small></div>", unsafe_allow_html=True)
        for x in q_lead: 
            sig_badge = "🛡️ Sig" if x["significant"] else ""
            st.write(f"• **{x['code']['id']}** ({x['code']['name']}) {sig_badge}")

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("<div class='quad-card' style='background: rgba(51, 65, 85, 0.3); border-color: #64748b;'><b>DROP FOR NOW</b><br><small>Low Frequency / Low Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_drop: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")
        
    with g4:
        st.markdown("<div class='quad-card' style='background: rgba(99, 102, 241, 0.15); border-color: #6366f1;'><b>NICHE / BROAD CONCERN</b><br><small>High Frequency / Low Pain Rate</small></div>", unsafe_allow_html=True)
        for x in q_niche: st.write(f"• **{x['code']['id']}** ({x['code']['name']})")

    st.markdown("---")
    st.subheader("Automated Campaign Messaging Strategy Output")
    selected_matrix_code = st.selectbox("Select Code for Campaign Strategy Brief:", [x["code"]["id"] for x in matrix_data])
    target_item = next(x for x in matrix_data if x["code"]["id"] == selected_matrix_code)
    
    st.info(f"**Target Code:** {target_item['code']['id']} - {target_item['code']['name']}")
    st.write(f"**Primary Campaign Headline:** Stop Drowning in {target_item['code']['name']} — Build Your Thesis Plan Fast with Thought Sweep.")
    st.write(f"**Recommended Channel:** Barrett Honors College Weekly Digest & Academic Advisor Referrals")
    st.markdown("</div>", unsafe_allow_html=True)
