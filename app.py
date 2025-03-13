

# # v3: after policy tool
# # app.py
# import streamlit as st
# from agent import create_agent

# def main():
#     st.title("LangChain Agent-Based Travel Assistant (with Policy)")

#     if "agent" not in st.session_state:
#         st.session_state.agent = create_agent()
#         st.session_state.chat_history = []

#     user_input = st.text_input("Ask me about flights (e.g., 'Find flights from Istanbul to Ankara'):")
#     if user_input:
#         st.session_state.chat_history.append(("User", user_input))
        
#         # Call the agent
#         response = st.session_state.agent.run(
#             input=user_input,
#             chat_history="\n".join([f"{speaker}: {content}" 
#                                     for speaker, content in st.session_state.chat_history]),
#         )

#         # Display the response
#         st.session_state.chat_history.append(("Assistant", response))
#         st.markdown(f"**Assistant:** {response}")

# if __name__ == "__main__":
#     main()



##### v5: after chatbot ui:

import streamlit as st
from agent import create_agent 

def main():
    st.title("LangChain Chatbot with History")

    # 1. Initialize Agent & Messages in Session State
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
        
        st.session_state.messages = [] # for chat history

    # 2. Display Existing Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 3. Chat Input Field (Streamlit automatically positions it at the bottom)
    user_input = st.chat_input("Ask me about flights...")  # The placeholder text

    if user_input:
        # 3A. Add the user's message to the conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 3B. Display the user's message immediately
        with st.chat_message("user"):
            st.write(user_input)

        # 4. Prepare the chat history in a format the agent can understand
        #    (For example: "User: Hello\nAssistant: Hi!\n...")
        formatted_history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )

        # 5. Run the agent with the current user_input and the full conversation
        response = st.session_state.agent.run(
            input=user_input,
            chat_history=formatted_history
        )

        # 6. Add the assistant's response to the conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 7. Display the assistant's message
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()

