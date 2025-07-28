import streamlit as st
import boto3
import openai
import tempfile
import fitz  # PyMuPDF for PDF text extraction
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# ✅ Load secrets
aws_access_key = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_REGION"]
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# ✅ Set OpenAI Key
openai.api_key = openai_api_key

# ✅ AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

bucket_name = "my-langchain-demo-bucket"

st.title("AWS + LangChain + OpenAI Demo")
st.write(f"✅ Connected to AWS Region: **{aws_region}**")

# ✅ Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # ✅ Upload to S3
    file_name = uploaded_file.name
    try:
        s3_client.upload_file(tmp_path, bucket_name, file_name)
        st.success(f"File uploaded to S3: {file_name}")
    except Exception as e:
        st.error(f"Upload failed: {e}")

    # ✅ Extract text from PDF
    with fitz.open(tmp_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    st.subheader("Extracted Text Preview")
    st.write(text[:1000] + "...")  # Show first 1000 chars

    # ✅ Q&A Section
    st.subheader("Ask a Question About Your PDF")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer") and question:
        llm = OpenAI(temperature=0.3, openai_api_key=openai_api_key)
        template = """
        You are a helpful assistant. Use the following text to answer the question.

        Context: {context}
        Question: {question}

        Answer:
        """
        prompt = PromptTemplate(input_variables=["context", "question"], template=template)
        final_prompt = prompt.format(context=text[:3000], question=question)

        answer = llm(final_prompt)
        st.write("### Answer:")
        st.write(answer)
