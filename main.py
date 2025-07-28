import streamlit as st
import boto3
import openai

# ✅ Read secrets from Streamlit
aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS_REGION"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Configure OpenAI
openai.api_key = openai_api_key

# ✅ Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# ✅ Streamlit UI
st.title("AWS + LangChain + OpenAI Demo")
st.write(f"✅ Connected to AWS Region: {aws_region}")

# ✅ File Upload Section
st.subheader("Upload a file to AWS S3")
uploaded_file = st.file_uploader("Drag and drop file here", type=["txt", "pdf"])

bucket_name = "my-langchain-demo-bucket"  # Change if needed

if uploaded_file is not None:
    file_name = uploaded_file.name
    try:
        s3_client.upload_fileobj(uploaded_file, bucket_name, file_name)
        st.success(f"✅ Uploaded {file_name} to S3 bucket: {bucket_name}")
    except Exception as e:
        st.error(f"Upload failed: {e}")

# ✅ OpenAI Integration Test
st.subheader("Test OpenAI Integration")

if st.button("Generate Welcome Message"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a welcome message for a LangChain + AWS demo app."}
            ]
        )
        st.write("### Response:")
        st.write(response["choices"][0]["message"]["content"])
    except Exception as e:
        st.error(f"Error: {e}")

# ✅ LangChain Q&A Section (Simplified Demo)
st.subheader("LangChain Q&A")
user_question = st.text_input("Ask a question:")

if st.button("Answer"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in AWS and AI."},
                    {"role": "user", "content": user_question}
                ]
            )
            st.write("### Answer:")
            st.write(response["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"Error: {e}")
