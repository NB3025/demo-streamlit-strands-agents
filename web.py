import streamlit as st
import json

from my_agent import MyAgent

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add title on the page
st.title("데모 제목입니다.")
st.write("데모 설명 페이지입니다.")
st.set_page_config(layout="wide")

my_agent = MyAgent()
# Initialize the agent
if "agent" not in st.session_state:
    st.session_state.agent = my_agent.get_agent()

if "start_index" not in st.session_state:
    st.session_state.start_index = 0


# Display old chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.empty()  # This forces the container to render without adding visible content (workaround for streamlit bug)
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your agent..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Clear previous tool usage details
    if "details_placeholder" in st.session_state:
        st.session_state.details_placeholder.empty()
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Get response from agent
    with st.spinner("Thinking..."):
        response = st.session_state.agent(prompt)
    
    assistant_response = ""
    for m in st.session_state.agent.messages:
        if m.get("role") == "assistant" and m.get("content"):
            for content_item in m.get("content", []):
                if "text" in content_item:
                    # We keep only the last response of the assistant
                    assistant_response = content_item["text"]
                    break
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        
        start_index = st.session_state.start_index      

        # Display last messages from agent, with tool usage detail if any
        st.session_state.details_placeholder = st.empty()  # Create a new placeholder
        with st.session_state.details_placeholder.container():
            for m in st.session_state.agent.messages[start_index:]:
                if m.get("role") == "assistant":
                    for content_item in m.get("content", []):
                        if "text" in content_item:
                            st.write(content_item["text"])
                        elif "toolUse" in content_item:
                            tool_use = content_item["toolUse"]
                            tool_name = tool_use.get("name", "")
                            tool_input = tool_use.get("input", {})
                            st.info(f"Using tool: {tool_name}")
                            st.code(json.dumps(tool_input, indent=2))
            
                elif m.get("role") == "user":
                    for content_item in m.get("content", []):
                        if "toolResult" in content_item:
                            tool_result = content_item["toolResult"]
                            st.info(f"Tool Result: {tool_result.get('status', '')}")
                            for result_content in tool_result.get("content", []):
                                if "text" in result_content:
                                    st.code(result_content["text"])

        # Update the number of previous messages
        st.session_state.start_index = len(st.session_state.agent.messages)
    

