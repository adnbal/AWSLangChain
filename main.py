import os
import streamlit as st
from langchain.chat_models import BedrockChat
from langchain.schema import HumanMessage, SystemMessage
import boto3

# Streamlit UI
st.set_page_config(page_title="AI Chatbot (Bedrock)", layout="centered")
st.title("🤖 AI Chatbot using Amazon Bedrock")

# AWS credentials from Streamlit secrets
aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS_REGION"]

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# LangChain Bedrock LLM
llm = BedrockChat(client=bedrock_client, model="anthropic.claude-v2")  # Change model if needed

# Conversation memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_area("Type your message:", placeholder="Ask me anything...")

if st.button("Send"):
    if user_input.strip():
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Prepare messages for LangChain
        messages = [SystemMessage(content="You are a helpful AI assistant.")]
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))

        # Get response
        response = llm(messages)
        bot_reply = response.content

        # Append bot response
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# Display chat
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"👤 **You:** {chat['content']}")
    else:
        st.markdown(f"🤖 **AI:** {chat['content']}")
