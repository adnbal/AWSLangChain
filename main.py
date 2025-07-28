import streamlit as st
import boto3
import openai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI

# ==============================
# ✅ Load Secrets from Streamlit
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

bucket_name = "my-langchain-demo-bucket"  # Change if needed

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
    if st.button("Upload to S3"):
        try:
            with st.spinner("Uploading to S3..."):
                uploaded_file.seek(0)  # ✅ Reset file pointer before upload
                s3_client.upload_fileobj(uploaded_file, bucket_name, uploaded_file.name)
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
        except Exception as e:
            st.error(f"Upload failed: {e}")

# ==============================
# ✅ Test OpenAI Integration
# ==============================
st.subheader("Test OpenAI Integration")

if st.button("Generate Welcome Message"):
    with st.spinner("Generating..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Write a short welcome message for an AI app using AWS and LangChain."}
                ],
                timeout=15
            )
            st.write(response.choices[0].message["content"])
        except Exception as e:
            st.error(f"Error: {e}")

# ==============================
# ✅ LangChain Q&A Demo
# ==============================
st.subheader("LangChain Q&A")
question = st.text_input("Ask a question:")

if st.button("Answer"):
    if question:
        with st.spinner("Thinking..."):
            try:
                llm = LangChainOpenAI(openai_api_key=openai_api_key, temperature=0.5)
                prompt = PromptTemplate(
                    input_variables=["question"],
                    template="You are an expert in AI and AWS. Answer the question: {question}"
                )
                chain = LLMChain(llm=llm, prompt=prompt)
                answer = chain.run(question=question)
                st.success(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question first.")
