from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
import os 
import pypdf
from dotenv import load_dotenv
import streamlit as st
import asyncio
from openai import AsyncOpenAI

load_dotenv()

API = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

# --- Normal PDF text extraction for UI ---
def extract_pdf_text_normal(file_path: str) -> str:
    """
    Reads and extracts text from a PDF file for UI display.
    """
    text = ""
    with open(file_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# --- Tool function for the Agent ---
@function_tool
def extract_pdf_text(file_path: str) -> str:
    """
    Reads and extracts text from a PDF file for the Agent.
    """
    return extract_pdf_text_normal(file_path)

# --- Agent Setup ---
@st.cache_resource
def get_agent():
    external_client = AsyncOpenAI(
    api_key=API,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
    )
    agent = Agent(
        model=model,
        name="StudyNotesAssistant",
        instructions="You are a Study Notes Assistant. First produce a summary, then generate a quiz.",
        tools=[extract_pdf_text],
    )
    return agent

# --- Streamlit UI ---
def run_streamlit_app():
    st.title("📚 Study Notes & Quiz Generator")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save uploaded PDF temporarily
        temp_dir = "temp_pdfs"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"PDF uploaded: {uploaded_file.name}")

        # Extract text for UI
        extracted_text = extract_pdf_text_normal(file_path)
        st.subheader("📄 Extracted Text:")
        st.text_area("PDF Content", extracted_text, height=300)

        # Initialize agent
        agent = get_agent()

        if agent and st.button("Generate Summary & Quiz"):
            st.info("Generating summary and quiz... This may take a moment.")
            
        async def run_agent_async():
           return await Runner.run(
            starting_agent=agent,
           input=f"Summarize this text and then create a quiz:\n\n{extracted_text}"
           )
        
        result = asyncio.run(run_agent_async())
        st.subheader("📝 Summary & Quiz:")
        st.write(result.final_output)

if __name__ == "__main__":
    run_streamlit_app()
