import streamlit as st
import boto3
import openai

# --- Load Secrets from Streamlit ---
aws_access_key = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_REGION"]
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# --- Configure OpenAI ---
openai.api_key = openai_api_key

# --- Configure AWS S3 Client ---
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# --- Streamlit UI ---
st.title("AWS + LangChain + OpenAI Demo")
st.write("✅ Connected to AWS Region:", aws_region)

# --- Upload File to AWS S3 ---
uploaded_file = st.file_uploader("Upload a file to AWS S3", type=["txt", "pdf"])
bucket_name = "your-s3-bucket-name"  # Replace with your bucket

if uploaded_file is not None:
    file_name = uploaded_file.name
    s3_client.upload_fileobj(uploaded_file, bucket_name, file_name)
    st.success(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}'")

# --- OpenAI Test Button ---
st.subheader("Test OpenAI Integration")
if st.button("Generate Welcome Message"):
    with st.spinner("Calling OpenAI..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a short welcome message for AWS LangChain demo."}
            ]
        )
        st.success(response["choices"][0]["message"]["content"])

# --- Optional LangChain Section ---
st.subheader("LangChain Q&A")
user_query = st.text_input("Ask a question (demo):")
if st.button("Answer"):
    if user_query.strip():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial assistant using LangChain."},
                {"role": "user", "content": user_query}
            ]
        )
        st.write("Answer:", response["choices"][0]["message"]["content"])
    else:
        st.warning("Please enter a question.")
