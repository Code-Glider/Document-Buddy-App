# new.py

import streamlit as st
import os
import tempfile
from vectors import EmbeddingsManager
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

# Set page configuration
st.set_page_config(
    page_title="Document Processing App",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📚 Document Processing App")
st.markdown("""
Process your documents and create embeddings for semantic search and analysis.
Upload your files and click process to begin.
""")

# Initialize EmbeddingsManager
embeddings_manager = EmbeddingsManager()

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # File uploader
    uploaded_file = st.file_uploader("Upload a document")

    if uploaded_file is not None:
        st.success("📄 File Uploaded Successfully!")
        st.markdown(f"**Filename:** {uploaded_file.name}")
        st.markdown(f"**File Size:** {uploaded_file.size} bytes")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Process button
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    result = embeddings_manager.create_embeddings(tmp_file_path)
                    st.success(result)
                    
                    # Add to processed files list
                    if uploaded_file.name not in st.session_state.processed_files:
                        st.session_state.processed_files.append(uploaded_file.name)
                        
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
            
            # Clean up temporary file
            os.unlink(tmp_file_path)

with col2:
    # Display processed files
    if st.session_state.processed_files:
        st.markdown("### Processed Files")
        for file in st.session_state.processed_files:
            st.markdown(f"✅ {file}")
    else:
        st.markdown("### No files processed yet")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Name")
