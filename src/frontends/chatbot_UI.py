from typing import Dict, List, Text

import streamlit as st
import requests
import json
from uuid import uuid4
import os

CHAT_API_URL = "http://localhost:8000/chat"
RESUME_API_URL = "http://localhost:8000/resume"
THREAD_ID = "t001"

# Increase timeout in debug mode
DEBUG_TIMEOUT = 300 if os.getenv("STREAMLIT_DEBUG") else 30


def send_message(messages: List[Dict[Text, Text]], thread_id: Text) -> Dict:
    headers = {"Content-Type": "application/json"}
    data = {"messages": messages, "thread_id": thread_id}
    try:
        response = requests.post(CHAT_API_URL, headers=headers, data=json.dumps(data), timeout=DEBUG_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to chat API. Make sure the FastAPI server is running on http://localhost:8000")
        return {"error": "Connection failed", "response": "API server not available"}
    except requests.exceptions.Timeout:
        st.error(f"❌ API request timed out after {DEBUG_TIMEOUT} seconds")
        return {"error": "Timeout", "response": f"Request took longer than {DEBUG_TIMEOUT} seconds"}
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API Error: {e.response.status_code} - {e.response.text}")
        return {"error": str(e), "response": f"HTTP Error {e.response.status_code}"}
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return {"error": str(e), "response": "An error occurred"}


def resume(approved: bool, thread_id: Text) -> Dict:
    headers = {"Content-Type": "application/json"}
    data = {"approved": approved, "thread_id": thread_id}
    try:
        response = requests.post(RESUME_API_URL, headers=headers, data=json.dumps(data), timeout=DEBUG_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to chat API. Make sure the FastAPI server is running.")
        return {"error": "Connection failed", "response": "API server not available"}
    except requests.exceptions.Timeout:
        st.error(f"❌ API request timed out after {DEBUG_TIMEOUT} seconds")
        return {"error": str(e), "response": f"Request took longer than {DEBUG_TIMEOUT} seconds"}
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API Error: {e.response.status_code} - {e.response.text}")
        return {"error": str(e), "response": f"HTTP Error {e.response.status_code}"}
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return {"error": str(e), "response": "An error occurred"}




st.title("Simple Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.awaiting_approval:
    st.warning("⚠️ The assistant wants to use a tool. Allow it?")

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button("✅ Allow"):
            st.session_state.awaiting_approval = False
            result = resume(True, thread_id=st.session_state.thread_id)
            st.session_state.messages.append(
                {"role": "assistant", "content": result["response"]}
            )
            st.chat_message("assistant").markdown(result["response"])
            st.rerun()
    with col2:
        if st.button("❌ Deny"):
            result = resume(False, thread_id=st.session_state.thread_id)
            st.session_state.awaiting_approval = False
            st.session_state.messages.append(
                {"role": "assistant", "content": result["response"]}
            )
            st.chat_message("assistant").markdown(result["response"])
            st.rerun()

# --- Normal chat input ---
elif prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    result = send_message(st.session_state.messages, thread_id=st.session_state.thread_id)
    
    if "error" in result:
        st.error(f"API Error: {result['error']}")
        st.rerun()
        
        
    if result.get("need_approval"):
      # Show what the agent said before pausing
      st.session_state.awaiting_approval = True
    else:
     
      with st.chat_message("assistant"):
         # Show what the agent said before pausing
          st.markdown(result["response"])
           # Add assistant response to chat history
          st.session_state.messages.append(
              {"role": "assistant", "content": result["response"]}
          )
          
    st.rerun()  
    
    
      

