"""
Casino Black Box - Evidence-Based Casino Testing Platform
Main Streamlit application
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Casino Black Box",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("🎰 Casino Black Box")
st.subheader("Evidence-Based Casino Testing & Accountability Platform")

# Sidebar navigation
st.sidebar.markdown("---")
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a page:",
    [
        "Home",
        "New Test Session",
        "View Sessions",
        "Casino Directory",
        "Reports",
        "Settings"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Casino Black Box** records what actually happens when you test an online casino. "
    "Don't trust advertised claims — we document the evidence."
)

# Page: Home
if page == "Home":
    st.markdown("""
    ## Welcome to Casino Black Box
    
    This platform helps you **test online casinos objectively** and **record complete evidence**.
    
    ### What we do:
    
    ✅ **Record the complete experience** — registration, bonuses, gameplay, deposits, withdrawals  
    ✅ **Calculate actual RTP** — compare what you observed vs. what was advertised  
    ✅ **Flag suspicious activity** — delays, restrictions, balance discrepancies  
    ✅ **Generate defensible reports** — with screenshots, data, and analysis  
    ✅ **Score casinos transparently** — across 12 key categories  
    
    ### Core principle:
    
    > **Do not trust advertised claims. Record what actually happened.**
    
    ---
    
    ### Quick Start
    
    1. **Create a new test session** — Enter casino details and test parameters
    2. **Record your activity** — Log deposits, bets, wins, withdrawals
    3. **Upload evidence** — Screenshots, receipts, chat logs, emails
    4. **Get analysis** — Calculated RTP, suspicious-activity flags, risk score
    5. **Generate report** — Professional PDF with complete evidence trail
    
    ---
    
    ### What Casino Black Box Tracks
    
    | Category | What We Record |
    |----------|----------------|
    | **Registration** | Speed, ease, document requirements |
    | **KYC** | Friction, delays, personal data requests |
    | **Bonuses** | Offer value, wagering requirements, restrictions |
    | **Games** | Selection, providers, stability |
    | **Gameplay** | Actual RTP, bet results, largest win |
    | **Deposits** | Speed, methods, fees |
    | **Withdrawals** | Processing time, delays, obstructions |
    | **Support** | Response time, quality, helpfulness |
    | **Trust** | Complaints, account restrictions, evidence quality |
    
    ---
    
    ### Important Notes
    
    ⚠️ **Statistical Variance**  
    A single short test cannot prove a game's RTP is false. We distinguish between:
    - A poor individual result
    - An unusual statistical result
    - A recurring pattern across many tests
    - Evidence of actual misconduct
    
    ⚠️ **Responsible Testing**  
    - Set a fixed test budget
    - Take breaks
    - Don't chase losses
    - Stop if you reach your limit
    
    ⚠️ **Evidence Integrity**  
    All original files and timestamps are preserved. Screenshots and data are linked to your test.
    """)

# Page: New Test Session
elif page == "New Test Session":
    st.header("Create New Test Session")
    
    with st.form("new_session_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Casino Information")
            casino_name = st.text_input("Casino Name *", placeholder="e.g., Example Casino")
            casino_website = st.text_input("Casino Website", placeholder="e.g., https://example-casino.com")
            casino_licence = st.text_input("Licence/Jurisdiction", placeholder="e.g., Malta (MGA), UK (UKGC)")
        
        with col2:
            st.subheader("Test Parameters")
            test_budget = st.number_input("Test Budget (USD) *", min_value=10.0, value=100.0, step=10.0)
            test_start_date = st.date_input("Test Start Date")
            test_notes = st.text_area("Initial Notes", placeholder="Any notes about why you're testing this casino...")
        
        st.markdown("---")
        st.subheader("Deposit & Bonus")
        
        col3, col4 = st.columns(2)
        
        with col3:
            bonus_offered = st.text_input("Bonus Offered", placeholder="e.g., 100% match up to $200")
            deposit_amount = st.number_input("Deposit Amount (USD)", min_value=0.0, step=10.0)
        
        with col4:
            bonus_received = st.number_input("Bonus Credit Received (USD)", min_value=0.0, step=10.0)
            wagering_requirement = st.text_input("Wagering Requirement", placeholder="e.g., 35x bonus")
        
        st.markdown("---")
        
        submitted = st.form_submit_button("Create Test Session", use_container_width=True)
        
        if submitted:
            if not casino_name or not test_budget:
                st.error("Please fill in all required fields marked with *")
            else:
                st.success(f"✅ Test session created for **{casino_name}**")
                st.info(f"Session budget: ${test_budget} | Start date: {test_start_date}")

# Page: View Sessions
elif page == "View Sessions":
    st.header("Your Test Sessions")
    st.info("No test sessions yet. Create one to get started!")

# Page: Casino Directory
elif page == "Casino Directory":
    st.header("Casino Directory")
    st.info("Casino directory coming soon. This will show all tested casinos and aggregate results.")

# Page: Reports
elif page == "Reports":
    st.header("Test Reports")
    st.info("Generate PDF reports of your casino tests with full evidence and analysis.")

# Page: Settings
elif page == "Settings":
    st.header("Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Storage")
        storage_location = st.text_input("Local storage path", value="./casino_data")
        st.caption("Where test data and screenshots are stored locally")
    
    with col2:
        st.subheader("Export & Privacy")
        export_format = st.selectbox("Default report format", ["PDF", "HTML", "CSV"])
        redact_personal = st.checkbox("Redact personal data in reports", value=True)
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved")
