import streamlit as st
from engine.visualizer import generate_mermaid_chart, render_mermaid
from engine.rag_logic import process_document


st.set_page_config(page_title="TechTrace AI", layout="wide")

st.title("🚀 TechTrace AI: Code-to-Concept")
st.markdown("### *Building the future of tech learning in Bharat*")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    mode = st.toggle("Explain Like I'm a Student", value=True)
    st.info("When enabled, AI simplifies complex architectural concepts.")
    
    # Placeholder for when your AWS credits arrive
    aws_key = st.text_input("Enter AWS Access Key (Optional for now)", type="password")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload Code or Docs")
    uploaded_file = st.file_uploader("Upload a Python file or Documentation PDF", type=['py', 'pdf'])
    
    if st.button("Analyze & Trace"):
        # Inside app.py, replace the 'if uploaded_file:' block with this:

        if uploaded_file:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            
            # Save the file first
            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())

            if file_ext == "pdf":
                st.sidebar.success("Document Received!")
                chunks = process_document(f"data/{uploaded_file.name}")
                st.sidebar.write(f"Processed {len(chunks)} knowledge blocks.")
            
            elif file_ext == "py":
                st.sidebar.success("Code Script Received!")
                # For now, we'll just read the text. Later, Bedrock will analyze it.
                with open(f"data/{uploaded_file.name}", "r") as f:
                    code_content = f.read()
                st.sidebar.write(f"Script loaded: {len(code_content)} characters.")
            
            else:
                st.error("Unsupported file type! Please upload .py or .pdf.")

with col2:
    st.subheader("📊 Logic Visualization")
    st.info("The dynamic Mermaid.js flow diagram will appear here.")