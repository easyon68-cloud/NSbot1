import streamlit as st
import openai

# Initialize OpenAI with your secret API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("🛠️ Network and Server Troubleshoot")

# Initialize chat history with a system prompt focused on IT troubleshooting
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

# Display all previous messages (excluding system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Describe your network or server issue...")

# Function to get AI response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Process user input
if user_input:
    # Add user's message to history and show
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response = get_response(st.session_state.messages)

    # Add assistant response to history and show
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Optional: Add footer disclaimer
st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This chatbot does not provide certified IT support or emergency services. "
    "Always consult your IT administrator or support team for critical infrastructure issues.",
    unsafe_allow_html=True
)
