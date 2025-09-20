import streamlit as st
import os
from src.modules.compliance_scanner import analyze_document_compliance
from src.utils.report_generator import handle_report_display_and_download 

def show_scanner():
    # Professional header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">Real-Time Compliance Scanner</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">
            Upload a requirements document to instantly identify compliance risks against international healthcare standards
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if GCP is configured
    if not os.getenv("GCP_PROJECT_ID"):
        st.error("""
        **Configuration Required**
        
        The Compliance Scanner requires Google Cloud Platform services to function. 
        Please ensure your `.env` file contains the required GCP configuration:
        
        ```
        GCP_PROJECT_ID=your-project-id
        GCP_REGION=us-central1
        DOCAI_PROCESSOR_ID=your-processor-id
        ```
        """)
        return

    # Standards selection with enhanced UI
    st.subheader("Compliance Standards")
    standards = {
        "India (DPDPA/CDSCO)": {
            "description": "Indian Digital Personal Data Protection Act (DPDPA) and CDSCO telemedicine guidelines",
            "expert_persona": "An expert on the Indian Digital Personal Data Protection Act (DPDPA) and CDSCO telemedicine guidelines.",
            "color": "#059669"
        },
        "USA (HIPAA/FDA)": {
            "description": "US Health Insurance Portability and Accountability Act (HIPAA) and FDA SaMD guidelines",
            "expert_persona": "An expert on the US Health Insurance Portability and Accountability Act (HIPAA) and FDA guidelines for software as a medical device (SaMD).",
            "color": "#dc2626"
        },
        "EU (GDPR/MDR)": {
            "description": "EU General Data Protection Regulation (GDPR) and Medical Device Regulation (MDR)",
            "expert_persona": "An expert on the EU General Data Protection Regulation (GDPR) and Medical Device Regulation (MDR).",
            "color": "#7c3aed"
        }
    }
    
    # Create tabs for standards selection
    tab1, tab2, tab3 = st.tabs(["🇮🇳 India (DPDPA)", "🇺🇸 USA (HIPAA/FDA)", "🇪🇺 EU (GDPR/MDR)"])
    
    with tab1:
        st.markdown(f"""
        <div style="padding: 1rem; border-left: 4px solid {standards['India (DPDPA/CDSCO)']['color']}; background: #f8fafc;">
            <h4 style="margin-top: 0; color: {standards['India (DPDPA/CDSCO)']['color']};">India (DPDPA/CDSCO)</h4>
            <p style="margin-bottom: 0; color: #6b7280;">{standards['India (DPDPA/CDSCO)']['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select India Standards", use_container_width=True, type="primary"):
            st.session_state.selected_standard = "India (DPDPA/CDSCO)"
            st.rerun()
    
    with tab2:
        st.markdown(f"""
        <div style="padding: 1rem; border-left: 4px solid {standards['USA (HIPAA/FDA)']['color']}; background: #f8fafc;">
            <h4 style="margin-top: 0; color: {standards['USA (HIPAA/FDA)']['color']};">USA (HIPAA/FDA)</h4>
            <p style="margin-bottom: 0; color: #6b7280;">{standards['USA (HIPAA/FDA)']['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select USA Standards", use_container_width=True, type="primary"):
            st.session_state.selected_standard = "USA (HIPAA/FDA)"
            st.rerun()
    
    with tab3:
        st.markdown(f"""
        <div style="padding: 1rem; border-left: 4px solid {standards['EU (GDPR/MDR)']['color']}; background: #f8fafc;">
            <h4 style="margin-top: 0; color: {standards['EU (GDPR/MDR)']['color']};">EU (GDPR/MDR)</h4>
            <p style="margin-bottom: 0; color: #6b7280;">{standards['EU (GDPR/MDR)']['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select EU Standards", use_container_width=True, type="primary"):
            st.session_state.selected_standard = "EU (GDPR/MDR)"
            st.rerun()
    
    # Initialize selected standard if not set
    if 'selected_standard' not in st.session_state:
        st.session_state.selected_standard = "India (DPDPA/CDSCO)"
    
    st.divider()
    
    # File upload section with enhanced styling
    st.subheader("Document Upload")
    
    with st.container(border=True):
        st.markdown("""
        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #374151;">Supported File Formats</h4>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <span style="background: #e5e7eb; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.875rem;">PDF</span>
                <span style="background: #e5e7eb; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.875rem;">DOCX</span>
                <span style="background: #e5e7eb; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.875rem;">TXT</span>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: #6b7280; font-size: 0.875rem;">
                Maximum file size: 10MB | Supported languages: English, Hindi
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a document to analyze", 
            type=["pdf", "docx", "txt"],
            help="Upload your requirements document for compliance analysis"
        )

    # Analysis section
    if uploaded_file is not None:
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully ({uploaded_file.size:,} bytes)")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
                with st.spinner("Executing compliance analysis... This may take a few moments."):
                    try:
                        file_content = uploaded_file.getvalue()
                        mime_type = uploaded_file.type
                        
                        # Get the selected standard
                        selected_standard = st.session_state.selected_standard
                        expert_persona = standards[selected_standard]['expert_persona']
                        
                        report = analyze_document_compliance(file_content, mime_type, expert_persona)
                        
                        # Store report and filename for reuse
                        st.session_state.scanner_report = report
                        st.session_state.scanner_filename = f"Compliance_Report_{uploaded_file.name.split('.')[0]}"
                        st.session_state.scanner_standard = selected_standard
                        
                        st.success("Analysis completed successfully!")
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        st.session_state.scanner_report = None
        
        with col2:
            st.info(f"**Selected Standard:** {st.session_state.selected_standard}")
    
    # Display and Download Section
    if 'scanner_report' in st.session_state and st.session_state.scanner_report:
        st.divider()
        st.subheader("Analysis Results")
        
        # Show analysis summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Standard Analyzed", st.session_state.get('scanner_standard', 'Unknown'))
        with col2:
            st.metric("Document Size", f"{uploaded_file.size:,} bytes" if uploaded_file else "Unknown")
        with col3:
            st.metric("Analysis Status", "Completed")
        
        handle_report_display_and_download(
            st.session_state.scanner_report,
            st.session_state.scanner_filename
        )