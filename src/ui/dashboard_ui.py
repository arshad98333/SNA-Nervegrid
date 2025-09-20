import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show_dashboard():
    # Professional header with gradient background
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">AI Compliance & Testing Co-Pilot</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Enterprise-grade automation for HealthTech compliance verification, test case generation, and synthetic data creation
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", "12", "3")
    with col2:
        st.metric("Compliance Checks", "156", "23")
    with col3:
        st.metric("Test Cases Generated", "2,847", "156")
    with col4:
        st.metric("Data Records Created", "45,231", "2,156")

    st.divider()

    # Core capabilities
    st.subheader("Core Capabilities")
    st.markdown("Select a tool below to begin your compliance and testing workflow:")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Compliance Scanner Card
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 1rem;">
                <h3 style="color: #2563eb; margin-top: 0;">Compliance Scanner</h3>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">
                    Instantly analyze requirement documents against global standards (DPDPA, FDA, GDPR) 
                    to identify risks before development begins.
                </p>
                <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem;">
                    <small style="color: #64748b;"><strong>Supported Standards:</strong> DPDPA, HIPAA, GDPR, MDR, FDA SaMD</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Access Compliance Scanner from sidebar", use_container_width=True, type="primary"):
                st.session_state.page = "Scanner"
                st.rerun()
        
        # Synthetic Data Hub Card
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 1rem;">
                <h3 style="color: #059669; margin-top: 0;">Synthetic Data Hub</h3>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">
                    Generate privacy-compliant, realistic data sets using natural language prompts, 
                    eliminating the risks associated with real PHI.
                </p>
                <div style="background: #f0fdf4; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem;">
                    <small style="color: #166534;"><strong>Features:</strong> HIPAA-compliant, customizable schemas, bulk generation</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Synthetic Data", use_container_width=True, type="primary"):
                st.session_state.page = "Data Hub"
                st.rerun()
    
    with col2:
        # Test Case Generator Card
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 1rem;">
                <h3 style="color: #dc2626; margin-top: 0;">Test Case Generator</h3>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">
                    Convert specifications into a complete, traceable test suite with a single click 
                    and export directly to enterprise tools like Jira.
                </p>
                <div style="background: #fef2f2; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem;">
                    <small style="color: #991b1b;"><strong>Integrations:</strong> Jira, Azure DevOps, TestRail, CSV Export</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Test Cases", use_container_width=True, type="primary"):
                st.session_state.page = "Test Generator"
                st.rerun()

        # AI Co-Pilot Card
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 1rem;">
                <h3 style="color: #7c3aed; margin-top: 0;">AI Co-Pilot</h3>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">
                    Your on-demand expert for regulatory questions. Get clear, concise answers 
                    from the AI chat assistant available in the sidebar.
                </p>
                <div style="background: #faf5ff; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem;">
                    <small style="color: #6b21a8;"><strong>Expertise:</strong> Global healthcare regulations, compliance best practices</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("Access the AI Co-Pilot from the sidebar for instant regulatory guidance.")

    # Recent activity section
    st.divider()
    st.subheader("Recent Activity")
    
    recent_activity = pd.DataFrame({
        'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(5)],
        'Action': ['Compliance Scan', 'Test Case Generation', 'Data Generation', 'Compliance Scan', 'Test Case Generation'],
        'Project': ['HealthApp v2.1', 'MediTrack Pro', 'PatientPortal', 'HealthApp v2.0', 'MediTrack Pro'],
        'Status': ['Completed', 'In Progress', 'Completed', 'Completed', 'Completed'],
        'Duration': ['2m 34s', 'Processing...', '1m 12s', '3m 45s', '2m 18s']
    })
    
    st.dataframe(recent_activity, use_container_width=True, hide_index=True)

    # Team Section
    st.divider()
    st.subheader("Meet the Team - SNA Nervegrid")

    team = [
        {
            "name": "Sowmya A M",
            "role": "HR Strategist",
            "gender": "female",
            "desc": "Specializes in people operations, organizational culture, and strategic HR initiatives."
        },
        {
            "name": "Naila Khan",
            "role": "UI-UX Designer",
            "gender": "female",
            "desc": "Crafts intuitive, human-centered interfaces with a strong focus on accessibility and user experience."
        },
        {
            "name": "Arshad Ahamed",
            "role": "AI Engineer",
            "gender": "male",
            "desc": "Builds intelligent AI-powered systems that bridge compliance automation with real-world healthcare needs."
        }
    ]

    col1, col2, col3 = st.columns(3)

    for i, member in enumerate(team):
        with [col1, col2, col3][i]:
            logo_url = "https://cdn-icons-png.flaticon.com/512/4140/4140048.png" if member["gender"] == "male" else "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"
            st.markdown(f"""
            <div style="text-align:center; padding:1rem; border-radius:10px; background:#f9fafb; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                <img src="{logo_url}" width="50" height="50" style="border-radius:50%; margin-bottom:0.5rem;" />
                <h4 style="margin:0; color:#111827;">{member['name']}</h4>
                <p style="margin:0; color:#2563eb; font-weight:600;">{member['role']}</p>
                <p style="margin-top:0.5rem; color:#4b5563; font-size:0.9rem;">{member['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
