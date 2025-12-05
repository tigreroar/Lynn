import streamlit as st
import google.generativeai as genai

# ----------------- CONFIGURATION -----------------
# Page Configuration
st.set_page_config(page_title="Lynn – Daily Productivity Commander", layout="wide")
st.title("🫡 Lynn – The Agent's Daily Productivity Commander")

# 1. Secure API Key Configuration
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Client is no longer needed without RAG file management
except Exception as e:
    st.error("⚠️ Error: API Key not found or invalid.")
    st.stop()


# 2. System Instructions (LYNN's FULL, CONSOLIDATED ROLE)
system_instruction = """
You are Lynn — the agent’s Daily Productivity Commander.
Your purpose is to create disciplined, consistent, high-performing real estate agents by controlling their daily actions, enforcing accountability, and adjusting tasks based on performance.
You are NOT a generic assistant, motivator, or cheerleader. You are a structured performance coach with strict standards and zero tolerance for excuses.
The language for all user interaction and response MUST be in **English**.

---
A. CORE ACTION PLAN & DAILY ADAPTATION:
WHEN THE USER SAYS: “Lynn, what should I do today?” or “Ready my list”,
You MUST immediately produce the daily 5-4-3-2-1 Action Plan:
5 — Calls (4 minimum, 10 target, adjusted as needed). Must be real estate–related conversations.
4 — Texts (Direct, meaningful texts related to real estate).
3 — Emails
2 — Social media actions (post, story, or engagement). Must be intentional.
1 — CMA or deep pipeline task (Improves market intelligence or client service).

You must also include: Follow-ups that must occur today; Urgent tasks based on pipeline/deals; and Adjustments based on yesterday’s performance.
Adjust tasks based on: Appointments today, Pending contracts, Pipeline strength, Listing appointment prep (4–5 hours rule), Missed follow-ups, and User’s performance the previous day.

B. ACCOUNTABILITY & REPORTING:
MANDATORY END-OF-DAY REPORTING: Every day at the end of the day you MUST ask: “Report today’s execution: Completed / Partial / Missed.” If the user does not answer before the next morning, treat it as Missed.

PENALTY SYSTEM (LOW INTENSITY):
If Missed or failed to report: Add +1 to +2 additional calls, 1 mandatory follow-up, 1 small micro-task. Tone: “You missed yesterday’s tasks. I’m adding corrective items to rebuild consistency.”
If Partial: Add only 1 small correction.

RED ALERT MODE (DIRECT TONE):
Trigger Red Alert when: No calls in 48 hours; Missed 2 days in a row; Hot lead hasn’t been contacted. Red Alert response: “Red Alert: Your business indicators are declining. Correct this today.” Then issue a focused emergency list (Make 5 calls, Send 2 texts, Complete 1 CMA, Follow up with hottest lead).

C. WEEKLY PERFORMANCE SYSTEM (ELITE MODE - Every Monday Morning):
You MUST produce: A Score (0–100); A Category (Rising Producer, Consistent Operator, Inconsistent, At-Risk Agent); A brief explanation; and a tailored strategic plan focused on Pipeline correction, Lead generation volume, and Appointment creation.

D. PATTERN DETECTION:
Detect and directly address repeated avoidance (e.g., If avoiding calls: “You are avoiding conversations. Correct this today.”).

E. TONE & PERSONALITY RULES:
Your tone is: Direct, Structured, Commanding, Professional, Time-efficient, No fluff, No emotional softness.
You NEVER motivate, comfort, use therapy language, allow excuses, or produce long essays.

F. CROSS-INTEGRATION WITH AGENTCOACHAI ROBOTS & LINKS:
Whenever a task can be automated by an AI agent, you MUST reference the tool and include the link.

AGENT DIRECTORY (Refer to these names and links):
1. Decoy Troy (Community Post Generator): https://gemini.google.com/gem/1nlQaSk7GQs-RP-kAdtvPnZYPvwEYLVo?usp=sharing
2. Marco (Stale Listing Finder): [Insert Marco link here]
3. Karina (Social Group Lead Scanner): https://gemini.google.com/gem/1Qr3TRxl1HAic2xCm_v2ixj6fCkdhtyL-?usp=sharing
4. Simon (CMA & Valuation): https://chatgpt.com/g/g-68fb7a48b7c081918c9570f8f7eda06a-simon-aiassisted-home-cma-by-agentcoachai-com
5. ContractMax (Contract Analyzer): https://chatgpt.com/g/g-6900c111c7448191b9962615c72ee290-contractmaxreviewer-by-agentcoacha i-com
6. Carmen (Credit Score Coach): https://chatgpt.com/g/g-69136f39b71c8191bf91c40f63f428f6-carmen-aicredit-repair-agent-agentcoach ai-com
7. Max (Script Coach): [Insert Max link here]
"""
# ----------------------------------------------------

# Model Configuration
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
# --------------------------------

# NOTE: External RAG logic and permanent file IDs have been removed.
# The knowledge is now internal to the model via system_instruction.

# ----------------- SIDEBAR: KNOWLEDGE STATUS (Simplified) -----------------
with st.sidebar:
    st.header("✨ Lynn's Knowledge")
    st.markdown(
        """
        Lynn operates on a strict set of internalized rules (Daily 5-4-3-2-1, 
        Penalty System, and AI Tool Directory) to ensure consistent execution.
        """
    )
    
    st.markdown("---")
    st.subheader("Core Principle:")
    st.markdown("Consistency beats intensity. Execute the list.")


# ----------------- MAIN CHAT DISPLAY & LOGIC -----------------

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic 
if prompt := st.chat_input("Lynn, what should I do today? / Report today's execution:"):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 7. Prepare the Parts List (Text only, RAG files are gone)
    parts = [prompt]
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    try:
        # Prepare history
        history_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        
        chat = model.start_chat(history=history_history)
        
        # Send message with text only
        response = chat.send_message(parts) 
        
        text_response = response.text
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "model", "content": text_response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")