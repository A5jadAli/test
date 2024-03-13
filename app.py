import streamlit as st
from my import my_main
# Check if "messages" key exists in the session state
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [{
        "role": "assistant", "content": "Hello, I am your assistant, how can I help you?"
    }]
if "messages" in st.session_state.keys():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Collect user input
user_input = st.chat_input("User Input")
if user_input is not None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
                mod_response = my_main(user_input)
                st.write(mod_response)

    new_mod_message = {"role": "assistant", "content": mod_response}
    st.session_state.messages.append(new_mod_message)
