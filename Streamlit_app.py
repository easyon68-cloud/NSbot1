import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the app title
st.title("🛠️ Network and Server Troubleshoot")

# Initialize chat history with a system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI assistant specialized in network and server troubleshooting. "
                "Your role is to help users diagnose common issues related to connectivity, server performance, configuration errors, and system logs. "
                "You must clearly state that you are not a certified technician and do not provide emergency IT support. "
                "If a user asks about anything unrelated to IT troubleshooting, reply: "
                "'I'm here to help with network and server troubleshooting. Please ask about connectivity issues, server errors, or system configurations.' "
                "If a user describes critical infrastructure failure or data breach, respond: "
                "'This may indicate a serious issue. Please contact your IT department or cybersecurity team immediately.'"
            )
        }
    ]

# Display previous messages (excluding system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# File upload section
uploaded_file = st.file_uploader("📁 Upload a log file for analysis", type=["txt", "log", "csv"])
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("📄 Log File Content", file_content, height=200)

    # Ask GPT to summarize the log
    summary_prompt = f"Please analyze and summarize the following troubleshooting log:\n\n{file_content}"
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes server and network logs."},
            {"role": "user", "content": summary_prompt}
        ]
    )
    st.subheader("🧾 Log Summary")
    st.write(summary_response.choices[0].message.content)

# Chat input
user_input = st.chat_input("Describe your network or server issue...")

# Function to get AI response
def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Handle user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Footer disclaimer
st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This chatbot does not provide certified IT support or emergency services. "
    "Always consult your IT administrator or support team for critical infrastructure issues.",
    unsafe_allow_html=True
)
``
