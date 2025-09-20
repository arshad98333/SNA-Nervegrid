import streamlit as st
from dotenv import load_dotenv
import os

# Only import the Co-Pilot at the top level as it's always needed for the sidebar.
from src.modules.ai_copilot import render_copilot

load_dotenv()

st.set_page_config(
    page_title="AI Compliance Co-Pilot for HealthTech",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Enterprise Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="st-"], button, input, textarea { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
    }
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --sidebar-background: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --border-hover: #cbd5e1;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
    }
    
    /* Main App Styling */
    .stApp { 
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--text-primary);
    }
    
    .main .block-container { 
        padding: 1rem 2rem 2rem;
        max-width: 100%;
        width: 100%;
    }
    
    /* Fix horizontal space issues */
    .stApp > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    .main .block-container > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background: var(--sidebar-background);
        border-right: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }
    
    [data-testid="stSidebar"] [data-testid="stHeader"] { 
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text-primary);
        padding: 1.5rem 1rem 1rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit branding */
    footer, #MainMenu, .stDeployButton, .stDecoration { 
        visibility: hidden; 
        display: none;
    }
    
    /* Button Styling */
    .stButton > button {
        font-weight: 600;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        background: var(--surface-color);
        color: var(--text-primary);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background: #f8fafc;
        border-color: var(--border-hover);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        outline: none;
        border-color: var(--primary-color);
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: var(--primary-hover);
        border-color: var(--primary-hover);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 { 
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.25;
    }
    
    h1 { font-size: 2.25rem; }
    h2 { font-size: 1.875rem; }
    h3 { font-size: 1.5rem; }
    h4 { font-size: 1.25rem; }
    
    /* Container Styling */
    .stContainer {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        background: var(--surface-color);
        box-shadow: var(--shadow-sm);
        padding: 1.5rem;
    }
    
    /* Metric Styling */
    [data-testid="metric-container"] {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        border: 2px dashed var(--border-color);
        border-radius: var(--radius-lg);
        background: #fafbfc;
        transition: all 0.2s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary-color);
        background: #f8fafc;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: var(--radius-md);
        color: var(--success-color);
    }
    
    .stError {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: var(--radius-md);
        color: var(--error-color);
    }
    
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: var(--radius-md);
        color: var(--warning-color);
    }
    
    .stInfo {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: var(--radius-md);
        color: var(--primary-color);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md);
        font-weight: 500;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
    }
    
    /* Spinner Styling */
    .stSpinner {
        color: var(--primary-color);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
    }
    
    /* LLM Generated Content Styling */
    .llm-content {
        text-align: justify;
        line-height: 1.5;
        font-size: 0.95rem;
        color: var(--text-primary);
        margin: 0.75rem 0;
    }
    
    .llm-content p {
        margin-bottom: 0.75rem;
        text-align: justify;
        line-height: 1.5;
    }
    
    .llm-content h1, .llm-content h2, .llm-content h3, .llm-content h4, .llm-content h5, .llm-content h6 {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        text-align: left;
        line-height: 1.25;
    }
    
    .llm-content ul, .llm-content ol {
        margin: 0.75rem 0;
        padding-left: 1.5rem;
    }
    
    .llm-content li {
        margin-bottom: 0.375rem;
        line-height: 1.5;
    }
    
    .llm-content blockquote {
        border-left: 4px solid var(--primary-color);
        padding-left: 1rem;
        margin: 1rem 0;
        font-style: italic;
        background: #f8fafc;
        padding: 0.75rem 1rem;
        border-radius: var(--radius-sm);
    }
    
    .llm-content code {
        background: #f1f5f9;
        padding: 0.125rem 0.375rem;
        border-radius: 4px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.875rem;
    }
    
    .llm-content pre {
        background: #f8fafc;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        padding: 1rem;
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    .llm-content pre code {
        background: none;
        padding: 0;
    }
    
    /* Report Content Styling */
    .report-content {
        text-align: justify;
        line-height: 1.5;
        font-size: 0.95rem;
        color: var(--text-primary);
        margin: 0.75rem 0;
        max-width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .report-content p {
        margin-bottom: 0.75rem;
        text-align: justify;
        line-height: 1.5;
    }
    
    .report-content h1, .report-content h2, .report-content h3, .report-content h4, .report-content h5, .report-content h6 {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        text-align: left;
        line-height: 1.25;
    }
    
    .report-content ul, .report-content ol {
        margin: 0.75rem 0;
        padding-left: 1.5rem;
    }
    
    .report-content li {
        margin-bottom: 0.375rem;
        line-height: 1.5;
    }
    
    .report-content strong {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .report-content em {
        font-style: italic;
        color: var(--text-secondary);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

    with st.sidebar:
        # Professional Sidebar Styling
        st.markdown("""
        <style>
        /* Professional Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stSidebar"] [data-testid="stHeader"] {
            background: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }
        
        .sidebar-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem 1rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .logo-icon::before {
            content: 'AI';
            font-size: 1rem;
            color: white;
            font-weight: bold;
        }
        
        .nav-container {
            padding: 0 1rem;
        }
        
        
        .nav-divider {
            height: 1px;
            background: #e2e8f0;
            margin: 1rem 0;
        }
        
        .sidebar-footer {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .footer-text {
            font-size: 0.75rem;
            color: #64748b;
            margin: 0;
        }
        
        /* Button styling overrides */
        .stButton > button {
            justify-content: flex-start !important;
            text-align: left !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: 1px solid #667eea !important;
            color: white !important;
        }
        
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid #e2e8f0 !important;
            color: #64748b !important;
        }
        
        .stButton > button:hover {
            transform: translateX(2px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Logo Section
        st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-icon"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Container
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # Navigation Items with Icons and Badges
        page_mapping = {
            "Dashboard": {"label": "Dashboard", "icon": "", "badge": None},
            "Scanner": {"label": "Compliance Scanner", "icon": "", "badge": None},
            "Test Generator": {"label": "Test Case Generator", "icon": "", "badge": None},
            "Data Hub": {"label": "Synthetic Data Hub", "icon": "", "badge": None},
            "AI Co-Pilot": {"label": "AI Co-Pilot", "icon": "", "badge": "NEW"}
        }
        
        # Create functional navigation using Streamlit buttons
        for page_key, page_info in page_mapping.items():
            is_active = st.session_state.page == page_key
            
            # Create button with custom styling
            button_style = f"""
            <style>
            .nav-button-{page_key.replace(' ', '-').lower()} {{
                width: 100%;
                background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if is_active else 'transparent'};
                color: {'white' if is_active else '#64748b'};
                border: 1px solid {'#667eea' if is_active else '#e2e8f0'};
                border-radius: 8px;
                padding: 0.75rem 1rem;
                margin: 0.25rem 0;
                font-weight: 500;
                font-size: 0.9rem;
                cursor: pointer;
                transition: all 0.2s ease;
                text-align: left;
                display: flex;
                align-items: center;
            }}
            .nav-button-{page_key.replace(' ', '-').lower()}:hover {{
                background: {'linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)' if is_active else '#e2e8f0'};
                transform: translateX(2px);
            }}
            </style>
            """
            st.markdown(button_style, unsafe_allow_html=True)
            
            # Create the button
            if st.button(f"{page_info['label']} {'NEW' if page_info['badge'] == 'NEW' else ''}", 
                        key=f"nav_{page_key}", 
                        use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.page = page_key
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
        
        # Footer
        # st.markdown("""
        # <div class="sidebar-footer">
            
        # </div>
        # """, unsafe_allow_html=True)

    # --- Resilient Page Routing with Lazy Imports ---
    # This prevents an error in one page from crashing the entire app.
    try:
        if st.session_state.page == "Dashboard":
            from src.ui.dashboard_ui import show_dashboard
            show_dashboard()
        elif st.session_state.page == "Scanner":
            from src.ui.scanner_ui import show_scanner
            show_scanner()
        elif st.session_state.page == "Test Generator":
            from src.ui.generator_ui import show_test_case_generator
            show_test_case_generator()
        elif st.session_state.page == "Data Hub":
            from src.ui.generator_ui import show_synthetic_data_generator
            show_synthetic_data_generator()
        elif st.session_state.page == "AI Co-Pilot":
            render_copilot()
            
    except ImportError as e:
        st.error(f"""
        **Application Error: Could not load page module.**

        A required component failed to import. This is often caused by a missing library.
        Please check your PowerShell terminal for a detailed traceback.
        
        **Common Fix:** Stop the app (Ctrl+C) and run `pip install -r requirements.txt` again.
        
        **Error Details:** `{e}`
        """)
    except Exception as e:
        st.error(f"""
        **An unexpected error occurred while rendering this page.**
        
        Please check the terminal for a full traceback to identify the issue.

        **Error Details:** `{e}`
        """)

if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ["GCP_PROJECT_ID", "GCP_REGION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"""
        **Configuration Error: Missing Environment Variables**
        
        The following required environment variables are not set:
        - {', '.join(missing_vars)}
        
        Please create a `.env` file in the project root with the following variables:
        ```
        GCP_PROJECT_ID=your-project-id
        GCP_REGION=us-central1
        DOCAI_PROCESSOR_ID=your-processor-id
        ```
        
        **Note:** This application requires Google Cloud Platform services to function properly.
        """)
    else:
        main()