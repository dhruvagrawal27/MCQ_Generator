import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.callbacks.manager import get_openai_callback
import PyPDF2

# Set page configuration
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better design
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4053;
        font-size: 3rem !important;
        padding-bottom: 2rem;
        text-align: center;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 5px;
        padding: 2rem;
        text-align: center;
    }
    .mcq-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .question {
        font-size: 1.1rem;
        font-weight: 500;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .options {
        margin-left: 20px;
    }
    .correct-answer {
        color: #27ae60;
        font-weight: 500;
        margin-top: 10px;
    }
    .explanation {
        color: #7f8c8d;
        font-style: italic;
        margin-top: 10px;
        padding: 10px;
        background-color: #f1f1f1;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Load response JSON
with open(r"F:\MCQ_Generator\response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)

# App Header
st.title("🎯 Interactive MCQ Generator")
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📄 Upload Your Document")
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop your PDF or TXT file here",
            type=['pdf', 'txt'],
            help="Supported formats: PDF, TXT"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### ⚙️ Configure Settings")
    with st.form("user_inputs"):
        # MCQ count with slider
        mcq_count = st.slider(
            "Number of MCQs",
            min_value=3,
            max_value=50,
            value=10,
            help="Select the number of questions you want to generate"
        )
        # Difficulty level with select box
        tone = st.selectbox(
            "Question Complexity",
            options=["Simple", "Moderate", "Complex"],
            help="Choose the difficulty level of questions"
        ).lower()
        # Generate button
        generate_button = st.form_submit_button("🚀 Generate MCQs")

# Process and display results
if generate_button and uploaded_file is not None:
    try:
        with st.spinner("🔮 Generating your MCQs..."):
            progress_bar = st.progress(0)

            # Read file
            text = read_file(uploaded_file)
            progress_bar.progress(30)

            # Generate MCQs
            with get_openai_callback() as cb:
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })
                progress_bar.progress(70)

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        progress_bar.progress(100)
                        st.success("✨ MCQs Generated Successfully!")

                        # Display statistics
                        st.markdown("### 📊 Generation Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Tokens", cb.total_tokens)
                        with col2:
                            st.metric("Prompt Tokens", cb.prompt_tokens)
                        with col3:
                            st.metric("Completion Tokens", cb.completion_tokens)
                        with col4:
                            st.metric("Cost ($)", round(cb.total_cost, 4))

                        # Display MCQs in interactive and table views
                        st.markdown("### 📝 Generated MCQs")
                        tabs = st.tabs(["Table View"])  # Get the list of tabs
                        
                        # Table View - use the first tab
                        with tabs[0]:  # Access the first tab using index
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.table(df)
                                st.download_button(
                                    label="📥 Download MCQs as CSV",
                                    data=df.to_csv(index=False),
                                    file_name="generated_mcqs.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.error("❌ Error in the table data")
                    else:
                        st.error("❌ No quiz data found in the response")
                else:
                    st.error("❌ Invalid response format")
    except Exception as e:
        st.error("❌ An error occurred!")
        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666; padding: 1rem;'>
        Made with ❤️ by Dhruv
    </div>
    """,
    unsafe_allow_html=True
)
