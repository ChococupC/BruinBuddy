import streamlit as st
import asyncio
from bruin_buddy import get_agent

# Custom CSS for UCLA colors with black background
st.markdown("""
<style>
/* Black background */
.stApp {
    background: linear-gradient(135deg, #2774AE 0%, #1a4d7a 30%, #FFD100 100%);
    background-attachment: fixed;
}

/* Chat container with dark background */
.stChatMessage {
    background-color: rgba(30, 30, 30, 0.95) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
    margin: 8px 0 !important;
    padding: 12px !important;
    box-shadow: 0 2px 8px rgba(255, 209, 0, 0.1) !important;
}

/* User message styling */
.stChatMessage[data-testid="chat-message-user"] {
    background-color: rgba(39, 116, 174, 0.2) !important;
    border-left: 3px solid #2774AE;
}

/* Assistant message styling */
.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: rgba(30, 30, 30, 0.95) !important;
    border-left: 3px solid #FFD100;
}

/* Avatar styling */
.st-emotion-cache-khw9fs {
    background-color: #2774AE !important;
}

.stChatMessage[data-testid="chat-message-assistant"] .stAvatar {
    background-color: #FFD100 !important;
}

/* Chat input container */
.stChatInputContainer {
    background-color: rgba(30, 30, 30, 0.95) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
    padding: 8px !important;
    box-shadow: 0 -2px 10px rgba(255, 209, 0, 0.1) !important;
}

.stChatInput input {
    border-color: #FFD100 !important;
    background-color: #1a1a1a !important;
    color: white !important;
}

.stChatInput input:focus {
    border-color: #FFD100 !important;
    box-shadow: 0 0 0 2px rgba(255, 209, 0, 0.3) !important;
}

.stChatInput button {
    background-color: #2774AE !important;
    border-color: #2774AE !important;
}

.stChatInput button:hover {
    background-color: #FFD100 !important;
}

/* Button styling */
.stButton > button {
    border-radius: 20px !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    background-color: #2774AE !important;
    color: white !important;
    border: 2px solid #FFD100 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background-color: #FFD100 !important;
    color: #000000 !important;
    border: 2px solid #2774AE !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 209, 0, 0.3) !important;
}

.stButton p {
    font-size: 13px !important;
    color: white !important;
}

/* Title styling */
h1 {
    color: #FFD100 !important;
    text-shadow: 2px 2px 4px rgba(39, 116, 174, 0.5);
    text-align: center;
    padding: 20px 0;
}

/* Message text color - WHITE */
.stChatMessage p {
    color: white !important;
}

/* Markdown in messages - WHITE */
.stChatMessage .stMarkdown {
    color: white !important;
}

.stChatMessage .stMarkdown h1,
.stChatMessage .stMarkdown h2,
.stChatMessage .stMarkdown h3,
.stChatMessage .stMarkdown h4 {
    color: #FFD100 !important;
}

.stChatMessage .stMarkdown strong {
    color: #FFD100 !important;
}

.stChatMessage .stMarkdown a {
    color: #2774AE !important;
}

.stChatMessage .stMarkdown a:hover {
    color: #FFD100 !important;
}

/* List styling */
.stChatMessage .stMarkdown ul,
.stChatMessage .stMarkdown ol {
    color: white !important;
}

.stChatMessage .stMarkdown li {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize the Strands agent (only once)
@st.cache_resource
def initialize_agent():
    return get_agent()

# Get the agent instance
agent = initialize_agent()

# Header
st.title("🐻 Bruin Buddy 🐻")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial AI greeting
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hey Bruin! 🐻💙 I'm here to help you navigate UCLA life. Whether you're looking for clubs to join, career resources, or general campus info—just ask! What can I help you with?"
    })
    
if "buttons_shown" not in st.session_state:
    st.session_state.buttons_shown = False

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show buttons embedded in first AI message only if not yet clicked
        if (
            i == 0 
            and message["role"] == "assistant" 
            and len(st.session_state.messages) == 1 
            and not st.session_state.buttons_shown
        ):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎯 Find Clubs"):
                    prompt = "I need help with school clubs and other available resources! Help me Bruin Buddy!"
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.buttons_shown = True
                    st.rerun()
            with col2:
                if st.button("💼 Career Resources"):
                    prompt = "I need help with career paths and other available resources! Help me Bruin Buddy!"
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.buttons_shown = True
                    st.rerun()

# Process pending user message (from button or chat input)
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    last_user_message = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        # Create placeholder for streaming response
        response_placeholder = st.empty()
        
        try:
            # Show initial acknowledgment
            response_placeholder.markdown("🐻💙 Looking into that for you...")
            
            # Async function to handle streaming
            async def stream_response():
                full_response = ""
                
                # Stream the agent response using stream_async()
                async for event in agent.stream_async(last_user_message):
                    if "data" in event:
                        # Accumulate text chunks
                        full_response += event["data"]
                        # Update display with cursor
                        response_placeholder.markdown(full_response + "▌")
                    elif "current_tool_use" in event and event["current_tool_use"].get("name"):
                        # Show tool usage (but keep it subtle)
                        response_placeholder.markdown("🐻💙 Looking into that for you...")
                
                return full_response
            
            # Run the async function
            full_response = asyncio.run(stream_response())
            
            # Final response without cursor
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            response_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Chat input
if prompt := st.chat_input("Ask me anything about UCLA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()