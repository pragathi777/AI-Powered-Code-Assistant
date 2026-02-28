import streamlit as st
from streamlit_ace import st_ace
from google import genai
from PIL import Image
import os
from dotenv import load_dotenv

# 1. Load Environment Variables & Configure Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Key not found. Please add it to your .env file.")
    st.stop()

# Initialize the NEW Google GenAI Client
client = genai.Client(api_key=API_KEY)

# 2. UI Configuration
st.set_page_config(page_title="Project-Aware AI Assistant", layout="wide")
st.title("🧠 Project-Aware Code Assistant")

# 3. Initialize Memory (Session State)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "project_context" not in st.session_state:
    st.session_state.project_context = ""

# 4. Sidebar: The "Eyes" and "Project Memory"
with st.sidebar:
    st.header("📁 Project Context")
    st.write("Upload your project files and error screenshots here so the AI understands the whole picture.")
    
    # File Uploader for Code Context
    uploaded_files = st.file_uploader(
        "Upload Code Files (.py, .js, .txt, etc.)", 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        context_string = ""
        for file in uploaded_files:
            try:
                content = file.read().decode("utf-8")
                context_string += f"--- File: {file.name} ---\n{content}\n\n"
            except Exception as e:
                st.error(f"Could not read {file.name}: {e}")
        st.session_state.project_context = context_string
        st.success(f"Loaded {len(uploaded_files)} files into memory.")

    # Image Uploader for Error Logs / Architecture Diagrams
    uploaded_image = st.file_uploader("Upload Error Screenshot or Diagram (jpg, png)", type=["png", "jpg", "jpeg"])
    img_context = None
    if uploaded_image:
        img_context = Image.open(uploaded_image)
        st.image(img_context, caption="Uploaded Image Context", use_container_width=True)

    if st.button("Clear History & Context"):
        st.session_state.chat_history = []
        st.session_state.project_context = ""
        st.rerun()

# 5. Main Interface Layout (Two Columns)
col1, col2 = st.columns([1, 1])

# Column 1: The Scratchpad (Streamlit-Ace)
with col1:
    st.subheader("📝 Live Scratchpad")
    st.write("Paste code here that you are currently working on.")
    editor_content = st_ace(
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        height=500,
    )

# Column 2: The Chat Interface
with col2:
    st.subheader("💬 Chat with AI")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    user_prompt = st.chat_input("Ask a question about your project...")

    if user_prompt:
        # Display user message instantly
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Build the mega-prompt with all context
        system_instructions = (
            "You are an expert, project-aware developer assistant. "
            "Use the provided project files, code scratchpad, and images to answer the user's query.\n\n"
        )
        
        full_prompt = [system_instructions]
        
        if st.session_state.project_context:
            full_prompt.append(f"### PROJECT FILES CONTEXT ###\n{st.session_state.project_context}\n")
        
        if editor_content:
            full_prompt.append(f"### CURRENT SCRATCHPAD CODE ###\n{editor_content}\n")
            
        full_prompt.append(f"### USER QUERY ###\n{user_prompt}")
        
        # Add the image to the prompt if one was uploaded
        if img_context:
            full_prompt.append(img_context)

        # Generate Response using the new SDK syntax
        with st.chat_message("assistant"):
            with st.spinner("Analyzing project context..."):
                try:
                    # The new client.models.generate_content method
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt
                    )
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")