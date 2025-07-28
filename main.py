import streamlit as st
import boto3
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --------------------------
# 1. Load Secrets from Streamlit
# --------------------------
aws_access_key = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_REGION"]

openai_api_key = st.secrets["OPENAI_API_KEY"]

# --------------------------
# 2. Initialize AWS Service (S3 as example)
# --------------------------
session = boto3.session.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)
s3 = session.client('s3')

# --------------------------
# 3. Streamlit UI
# --------------------------
st.title("AWS + LangChain Demo App")
st.write("This app uses **AWS S3** and **LangChain** with OpenAI to generate insights.")

# List buckets as a quick AWS test
try:
    buckets = s3.list_buckets()
    st.subheader("✅ Connected to AWS S3")
    for bucket in buckets['Buckets']:
        st.write(f"- {bucket['Name']}")
except Exception as e:
    st.error(f"Error connecting to AWS: {e}")

# --------------------------
# 4. LangChain + OpenAI
# --------------------------
st.subheader("AI Question Answering with OpenAI & LangChain")
user_input = st.text_area("Ask a question about AWS or anything:")

if st.button("Generate Answer"):
    if user_input.strip():
        try:
            llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
            prompt = PromptTemplate(
                input_variables=["question"],
                template="You are an expert. Answer this question: {question}"
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.run(question=user_input)
            st.success(response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.warning("Please enter a question.")
