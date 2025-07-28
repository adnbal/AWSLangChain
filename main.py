import streamlit as st
import boto3
from openai import OpenAI

# ✅ Load Secrets from Streamlit Secrets Manager
aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS_REGION"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)

# ✅ Initialize OpenAI Client
client = OpenAI(api_key=openai_api_key)

# ✅ Streamlit UI
st.title("AWS + LangChain + OpenAI Demo")
st.write(f"✅ Connected to AWS Region: **{aws_region}**")

# ✅ File Upload to S3
st.subheader("Upload a file to AWS S3")
uploaded_file = st.file_uploader("Drag and drop or Browse", type=["txt", "pdf"])
bucket_name = "my-langchain-demo-bucket"  # Change if needed

if uploaded_file:
    try:
        file_name = uploaded_file.name
        s3_client.upload_fileobj(uploaded_file, bucket_name, file_name)
        st.success(f"✅ Uploaded **{file_name}** to bucket: **{bucket_name}**")
    except Exception as e:
        st.error(f"Upload failed: {e}")

# ✅ Test OpenAI Integration
st.subheader("Test OpenAI Integration")

if st.button("Generate Welcome Message"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can switch to gpt-4 or gpt-4o
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a welcome message for a LangChain + AWS demo app."},
            ],
        )
        st.success("✅ OpenAI Response:")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")

# ✅ LangChain Q&A Section (Basic for Now)
st.subheader("LangChain Q&A")
question = st.text_input("Ask a question about your data:")

if st.button("Answer"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant answering general questions."},
                {"role": "user", "content": question},
            ],
        )
        st.success("✅ Answer:")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")
