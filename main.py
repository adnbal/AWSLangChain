import streamlit as st
import boto3
import openai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI

# ==============================
# ✅ Load Secrets
# ==============================
aws_access_key = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_REGION"]
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# Set OpenAI API key
openai.api_key = openai_api_key

# ==============================
# ✅ AWS S3 Client
# ==============================
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

bucket_name = "my-langchain-demo-bucket"  # <-- Use your bucket name

# ==============================
# ✅ Streamlit UI
# ==============================
st.title("AWS + LangChain + OpenAI Demo")

st.markdown(f"✅ Connected to AWS Region: **{aws_region}**")

# ==============================
# ✅ File Upload Section
# ==============================
uploaded_file = st.file_uploader("Upload a file to AWS S3", type=["txt", "pdf"])

if uploaded_file:
    file_name = uploaded_file.name
    try:
        s3_client.upload_fileobj(uploaded_file, bucket_name, file_name)
        st.success(f"✅ File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}'.")
    except Exception as e:
        st.error(f"Upload failed: {e}")

# ==============================
# ✅ OpenAI Integration Test
# ==============================
st.subheader("Test OpenAI Integration")

if st.button("Generate Welcome Message"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Write a short welcome message for an AI app using AWS and LangChain."}]
    )
    st.write(response.choices[0].message["content"])

# ==============================
# ✅ LangChain Q&A Demo
# ==============================
st.subheader("LangChain Q&A")

question = st.text_input("Ask a question (demo):")

if st.button("Answer"):
    if question:
        llm = LangChainOpenAI(openai_api_key=openai_api_key, temperature=0.5)
        prompt = PromptTemplate(
            input_variables=["question"],
            template="You are an expert in AI and AWS. Answer the question: {question}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        answer = chain.run(question=question)
        st.success(answer)
    else:
        st.warning("Please enter a question first.")
