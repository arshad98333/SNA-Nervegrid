import streamlit as st
import pandas as pd
from src.modules import test_case_generator, synthetic_data_hub
from src.services import jira_integration

def show_test_case_generator():
    # Professional header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">Automated Test Case Generator</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">
            Convert requirements documents into structured test suites and export seamlessly to your ALM platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if GCP is configured
    import os
    if not os.getenv("GCP_PROJECT_ID"):
        st.error("""
        **Configuration Required**
        
        The Test Case Generator requires Google Cloud Platform services to function. 
        Please ensure your `.env` file contains the required GCP configuration.
        """)
        return

    # File upload section
    st.subheader("Requirements Document Upload")
    
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
                Maximum file size: 10MB | AI will extract requirements and generate comprehensive test cases
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a requirements document", 
            type=["pdf", "docx", "txt"],
            help="Upload your requirements document for test case generation"
        )

        if uploaded_file:
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully ({uploaded_file.size:,} bytes)")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🧪 Generate Test Cases", use_container_width=True, type="primary"):
                    with st.spinner("AI is analyzing requirements and building your test suite..."):
                        try:
                            file_content = uploaded_file.getvalue()
                            test_cases_df = test_case_generator.generate_test_cases_from_doc(file_content, uploaded_file.type)
                            st.session_state.test_cases_df = test_cases_df
                            st.session_state.test_cases_filename = uploaded_file.name
                            st.success("Test cases generated successfully!")
                        except Exception as e:
                            st.error(f"Generation failed: {str(e)}")
                            st.session_state.test_cases_df = None
            
            with col2:
                st.info("**Ready to generate comprehensive test cases from your requirements document**")
    
    # Display generated test cases
    if 'test_cases_df' in st.session_state and st.session_state.test_cases_df is not None:
        st.divider()
        st.subheader("Generated Test Suite")
        
        # Show summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Test Cases", len(st.session_state.test_cases_df))
        with col2:
            positive_cases = len(st.session_state.test_cases_df[st.session_state.test_cases_df['type'].str.contains('positive', case=False, na=False)])
            st.metric("Positive Cases", positive_cases)
        with col3:
            negative_cases = len(st.session_state.test_cases_df[st.session_state.test_cases_df['type'].str.contains('negative', case=False, na=False)])
            st.metric("Negative Cases", negative_cases)
        with col4:
            edge_cases = len(st.session_state.test_cases_df[st.session_state.test_cases_df['type'].str.contains('edge', case=False, na=False)])
            st.metric("Edge Cases", edge_cases)
        
        # Display the test cases table
        st.dataframe(st.session_state.test_cases_df, use_container_width=True, height=400)

        # Export options
        st.subheader("Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            csv_data = st.session_state.test_cases_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Download as CSV",
                csv_data,
                f"test_cases_{st.session_state.test_cases_filename.split('.')[0]}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel Export
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state.test_cases_df.to_excel(writer, index=False, sheet_name='Test Cases')
            excel_data = output.getvalue()
            
            st.download_button(
                "📈 Download as Excel",
                excel_data,
                f"test_cases_{st.session_state.test_cases_filename.split('.')[0]}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        # Jira Integration
        with st.expander("🔗 Export to Jira", expanded=False):
            st.markdown("**Configure Jira Integration**")
            
            col1, col2 = st.columns(2)
            with col1:
                jira_url = st.text_input("Jira URL", "https://your-domain.atlassian.net", help="Your Jira instance URL")
                jira_email = st.text_input("Jira Email", help="Your Jira account email")
            with col2:
                jira_token = st.text_input("Jira API Token", type="password", help="Generate from Jira Account Settings > Security > API tokens")
                jira_project_key = st.text_input("Jira Project Key", "PROJ", help="The project key where test cases will be created")
            
            if st.button("🚀 Export to Jira", use_container_width=True, type="primary"):
                if not all([jira_url, jira_email, jira_token, jira_project_key]):
                    st.warning("Please fill in all Jira details to export.")
                else:
                    with st.spinner(f"Exporting {len(st.session_state.test_cases_df)} test cases to Jira project '{jira_project_key}'..."):
                        try:
                            success, message = jira_integration.export_test_cases_to_jira(
                                st.session_state.test_cases_df,
                                jira_url,
                                jira_email,
                                jira_token,
                                jira_project_key
                            )
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                        except Exception as e:
                            st.error(f"Export failed: {str(e)}")

def show_synthetic_data_generator():
    # Professional header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">On-Demand Synthetic Data Hub</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">
            Generate privacy-compliant, artificial data for testing using natural language prompts
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if GCP is configured
    import os
    if not os.getenv("GCP_PROJECT_ID"):
        st.error("""
        **Configuration Required**
        
        The Synthetic Data Hub requires Google Cloud Platform services to function. 
        Please ensure your `.env` file contains the required GCP configuration.
        """)
        return

    # Prompt templates section
    st.subheader("Data Generation Templates")
    
    # Create tabs for different data types
    tab1, tab2, tab3, tab4 = st.tabs([" Patient Data", " Medical Records", " Analytics Data", " Custom"])
    
    with tab1:
        st.markdown("""
        <div style="padding: 1rem; background: #f0fdf4; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #166534;">Patient Data Templates</h4>
            <p style="margin-bottom: 0; color: #166534;">Generate HIPAA-compliant patient profiles for various medical conditions</p>
        </div>
        """, unsafe_allow_html=True)
        
        template_options = {
            "Diabetes Management": "Generate 50 patient profiles for a diabetes management app. Include columns for patient_id, name, age, gender, blood_sugar_level (mg/dL), current_medication, diagnosis_date, and last_checkup. Ensure realistic age distribution and medication variety.",
            "Cardiology Patients": "Generate 30 cardiac patient profiles with columns for patient_id, name, age, gender, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, cholesterol_level, and prescribed_medications. Include various cardiac conditions.",
            "Mental Health": "Generate 25 mental health patient profiles with columns for patient_id, name, age, gender, diagnosis, severity_level, therapy_sessions, medication, and last_appointment. Ensure privacy-compliant data."
        }
        
        selected_template = st.selectbox("Select a template:", list(template_options.keys()))
        if st.button("Use Template", key="patient_template"):
            st.session_state.data_prompt = template_options[selected_template]
            st.rerun()
    
    with tab2:
        st.markdown("""
        <div style="padding: 1rem; background: #fef2f2; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #991b1b;">Medical Records Templates</h4>
            <p style="margin-bottom: 0; color: #991b1b;">Generate structured medical records and clinical data</p>
        </div>
        """, unsafe_allow_html=True)
        
        template_options = {
            "Lab Results": "Generate 100 lab test results with columns for test_id, patient_id, test_name, result_value, normal_range, units, test_date, and lab_name. Include various common tests like CBC, lipid panel, and metabolic panel.",
            "Prescription Records": "Generate 75 prescription records with columns for prescription_id, patient_id, medication_name, dosage, frequency, start_date, end_date, prescribing_doctor, and pharmacy_name.",
            "Appointment Records": "Generate 200 appointment records with columns for appointment_id, patient_id, doctor_name, specialty, appointment_date, duration_minutes, status, and notes."
        }
        
        selected_template = st.selectbox("Select a template:", list(template_options.keys()), key="medical_templates")
        if st.button("Use Template", key="medical_template"):
            st.session_state.data_prompt = template_options[selected_template]
            st.rerun()
    
    with tab3:
        st.markdown("""
        <div style="padding: 1rem; background: #faf5ff; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #6b21a8;">Analytics Data Templates</h4>
            <p style="margin-bottom: 0; color: #6b21a8;">Generate data for analytics and reporting purposes</p>
        </div>
        """, unsafe_allow_html=True)
        
        template_options = {
            "Usage Analytics": "Generate 500 user interaction records with columns for user_id, session_id, page_visited, time_spent_seconds, action_type, device_type, and timestamp. Include realistic usage patterns.",
            "Performance Metrics": "Generate 1000 system performance records with columns for timestamp, cpu_usage, memory_usage, response_time_ms, error_count, and active_users. Include realistic performance variations.",
            "Business Metrics": "Generate 365 daily business metrics with columns for date, new_users, active_users, revenue, support_tickets, and feature_adoption_rate. Include seasonal variations."
        }
        
        selected_template = st.selectbox("Select a template:", list(template_options.keys()), key="analytics_templates")
        if st.button("Use Template", key="analytics_template"):
            st.session_state.data_prompt = template_options[selected_template]
            st.rerun()
    
    with tab4:
        st.markdown("""
        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #374151;">Custom Data Generation</h4>
            <p style="margin-bottom: 0; color: #6b7280;">Describe your data requirements in natural language</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(" **Tips for better results:** Be specific about the number of records, column names, data types, and any constraints or patterns you want.")

    st.divider()

    # Data generation section
    st.subheader("Generate Synthetic Data")
    
    with st.container(border=True):
        # Initialize prompt if not set
        if 'data_prompt' not in st.session_state:
            st.session_state.data_prompt = "Generate 20 patient profiles from Mumbai for a diabetes management app. Include columns for patient_id, name, age, gender, blood_sugar_level (mg/dL), and current_medication. Ensure some patients are on Metformin."
        
        user_prompt = st.text_area(
            "Data Generation Prompt:", 
            value=st.session_state.data_prompt, 
            height=150,
            help="Describe the data you want to generate. Be specific about columns, data types, and constraints."
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(" Generate Data", type="primary", use_container_width=True):
                with st.spinner("AI is generating your synthetic dataset..."):
                    try:
                        json_str, df = synthetic_data_hub.generate_synthetic_data(user_prompt)
                        st.session_state.synthetic_data_json = json_str
                        st.session_state.synthetic_data_df = df
                        st.success("Data generated successfully!")
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")
                        st.session_state.synthetic_data_df = None
        
        with col2:
            st.info("**Ready to generate privacy-compliant synthetic data based on your requirements**")

    # Display generated data
    if 'synthetic_data_df' in st.session_state and st.session_state.synthetic_data_df is not None:
        st.divider()
        st.subheader("Generated Data Preview")
        
        # Show summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(st.session_state.synthetic_data_df))
        with col2:
            st.metric("Columns", len(st.session_state.synthetic_data_df.columns))
        with col3:
            st.metric("Data Size", f"{st.session_state.synthetic_data_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Display the data
        st.dataframe(st.session_state.synthetic_data_df, use_container_width=True, height=400)
        
        # Export options
        st.subheader("Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            csv_data = st.session_state.synthetic_data_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Download as CSV",
                csv_data,
                "synthetic_data.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON Export
            st.download_button(
                "📋 Download as JSON",
                st.session_state.synthetic_data_json,
                "synthetic_data.json",
                "application/json",
                use_container_width=True
            )
        
        with col3:
            # Excel Export
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state.synthetic_data_df.to_excel(writer, index=False, sheet_name='Synthetic Data')
            excel_data = output.getvalue()
            
            st.download_button(
                "📈 Download as Excel",
                excel_data,
                "synthetic_data.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )