import streamlit as st
from src.services import gcp_vertex_ai
import time

def render_copilot():
    """
    Renders the AI Co-Pilot chat interface with enterprise-grade design
    and enhanced user experience.
    """
    
    # Professional Enterprise Styling for AI Co-Pilot
    st.markdown("""
    <style>
        /* AI Co-Pilot Professional Styling */
        .ai-copilot-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .ai-copilot-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            border-radius: 20px;
        }
        
        .ai-copilot-header {
            position: relative;
            z-index: 2;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .ai-copilot-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: -0.02em;
        }
        
        .ai-copilot-subtitle {
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-weight: 400;
            letter-spacing: 0.01em;
        }
        
        .ai-copilot-icon {
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .ai-copilot-icon::before {
            content: '🤖';
            font-size: 2rem;
        }
        
        .quick-actions {
            display: flex;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .quick-action-btn {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            text-decoration: none;
            display: inline-block;
        }
        
        .quick-action-btn:hover {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            min-height: 500px;
            position: relative;
        }
        
        .chat-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #f1f5f9;
        }
        
        .chat-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #059669;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #059669;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .welcome-message {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            text-align: center;
            position: relative;
        }
        
        .welcome-message::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 16px;
            z-index: -1;
        }
        
        .welcome-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
        }
        
        .welcome-text {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.6;
            margin: 0;
        }
        
        .chat-input-container {
            position: sticky;
            bottom: 0;
            background: white;
            padding: 1.5rem 0 0;
            border-top: 1px solid #e2e8f0;
            margin-top: 2rem;
        }
        
        .chat-input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 50px;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        .chat-input-wrapper:focus-within {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .chat-input {
            flex: 1;
            border: none;
            background: transparent;
            outline: none;
            font-size: 1rem;
            color: #1e293b;
            padding: 0.5rem 0;
        }
        
        .chat-input::placeholder {
            color: #94a3b8;
        }
        
        .send-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-left: 1rem;
        }
        
        .send-button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .send-button:active {
            transform: scale(0.95);
        }
        
        /* Enhanced Chat Message Styling */
        [data-testid="stChatMessage"] {
            margin: 1rem 0;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
            text-align: left;
            line-height: 1.6;
            font-size: 1rem;
            padding: 1rem 1.5rem;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
            text-align: left;
            line-height: 1.6;
            margin-bottom: 0.75rem;
            color: #1e293b;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] h1,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] h2,
        [data-testid="stChatMessage"] div[data-testid="stChatMessage"] h3,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] h4,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] h5,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] h6 {
            text-align: left;
            line-height: 1.25;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: #1e293b;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] ul,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] ol {
            margin: 0.75rem 0;
            padding-left: 1.5rem;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] li {
            margin-bottom: 0.375rem;
            line-height: 1.6;
            color: #1e293b;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] strong {
            font-weight: 700;
            color: #667eea;
        }
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] code {
            background: #f1f5f9;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.875rem;
            color: #667eea;
            border: 1px solid #e2e8f0;
        }
        
        /* User message styling */
        [data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stChatMessage"][data-testid="stChatMessage-user"] div[data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        /* Assistant message styling */
        [data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }
        
        /* Spinner styling */
        .stSpinner {
            color: #667eea;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .ai-copilot-container {
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            
            .ai-copilot-title {
                font-size: 2rem;
            }
            
            .quick-actions {
                flex-direction: column;
                align-items: center;
            }
            
            .quick-action-btn {
                width: 100%;
                max-width: 300px;
            }
            
            .chat-container {
                padding: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize chat history with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Welcome to the AI Compliance Co-Pilot. I'm here to assist you with regulatory questions, compliance guidance, and best practices for healthcare software development. How may I help you today?"
        }]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process user input
    if user_prompt := st.chat_input("Ask about ALL regulations..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting regulatory models..."):
                
                # --- Guardrail and Alignment Prompt Engineering ---
                expert_prompt = f"""
                **SYSTEM INSTRUCTIONS:**
                1.  **Persona:** You are an expert AI assistant specializing in global healthcare software compliance (DPDPA, HIPAA, GDPR, etc.).
                2.  **Primary Directive: CONCISENESS.** Your response MUST be under 100 words and between 300-500 characters. This is a strict constraint. Do not exceed this limit.
                3.  **Tone:** Formal, professional, and direct.
                4.  **Formatting:** Use simple Markdown (bolding for emphasis). Do not use lists unless absolutely necessary for clarity within the character limit.
                5.  **Safety:** Do not provide legal advice. If asked for legal advice, politely state that you are an informational tool and recommend consulting a qualified professional.
                
                **USER QUERY:**
                "{user_prompt}"
                """
                
                response = gcp_vertex_ai.generate_text(expert_prompt)
                
                # --- Post-generation check (optional but good practice) ---
                # Although the prompt is strong, a final check can enforce the hard limit.
                if len(response) > 550: # Give a small buffer
                    response = response[:520] + "..."

                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})