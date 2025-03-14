

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



# ##### v5: after chatbot ui:

# import streamlit as st
# from agent import create_agent 

# def main():
#     st.title("LangChain Chatbot with History")

#     # 1. Initialize Agent & Messages in Session State
#     if "agent" not in st.session_state:
#         st.session_state.agent = create_agent()
        
#         st.session_state.messages = [] # for chat history

#     # 2. Display Existing Messages
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # 3. Chat Input Field (Streamlit automatically positions it at the bottom)
#     user_input = st.chat_input("Ask me about flights...")  # The placeholder text

#     if user_input:
#         # 3A. Add the user's message to the conversation history
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         # 3B. Display the user's message immediately
#         with st.chat_message("user"):
#             st.write(user_input)

#         # 4. Prepare the chat history in a format the agent can understand
#         #    (For example: "User: Hello\nAssistant: Hi!\n...")
#         formatted_history = "\n".join(
#             f"{m['role'].capitalize()}: {m['content']}"
#             for m in st.session_state.messages
#         )

#         # 5. Run the agent with the current user_input and the full conversation
#         response = st.session_state.agent.run(
#             input=user_input,
#             chat_history=formatted_history
#         )

#         # 6. Add the assistant's response to the conversation history
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # 7. Display the assistant's message
#         with st.chat_message("assistant"):
#             st.write(response)

# if __name__ == "__main__":
#     main()



###### v6: after purchase 

# app.py
import streamlit as st
from agent import create_agent
import ast

def main():
    st.title("LangChain Travel Assistant")

    # 1. Create/Load Agent & Session State
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
        st.session_state.messages = []  # for chat
        st.session_state.found_flights = []  # store last search results
        st.session_state.selected_flight = None

    # 2. Display existing messages in a chat format
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 3. Chat input
    user_input = st.chat_input("Ask me about flights or say 'I want to purchase a ticket'...")
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Build a text version of chat history for the agent
        formatted_history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )

        # 4. Call the agent
        response = st.session_state.agent.run(
            input=user_input,
            chat_history=formatted_history
        )

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

        # 5. Check if the agent's response includes flight data
        #    (For example, if the user asked for a flight search, we might parse them out ourselves.)
        #    This is optional. If the agent itself only returns text, you can skip.
        #    Otherwise, you might want to store the "found flights" in st.session_state.found_flights
        #    by parsing from the agent's tool usage logs or response. 
        #
        # For demonstration, we won't parse flights directly from the LLM's text.
        # Instead, we handle flight search in the LLM's step, which might list them in text form.

    st.divider()

    # 6. Optional: If you want to show flight results and pick one in the UI
    #    Let's assume st.session_state.found_flights is a list of flight dicts from a prior search.
    #    For demonstration, we'll just create some sample flights manually if none exist.

    if not st.session_state.found_flights:
        st.session_state.found_flights = [
            {
                "flight_code": "TK103",
                "carrier": "THY",
                "departure_city": "Istanbul",
                "arrival_city": "Ankara",
                "class": "Economy",
                "price": 1950
            },
            {
                "flight_code": "TK104",
                "carrier": "THY",
                "departure_city": "Istanbul",
                "arrival_city": "Ankara",
                "class": "Business",
                "price": 4150
            },
        ]

    st.write("### Available Flight Options (Example)")
    flight_options = [f"{f['flight_code']} - {f['carrier']} - {f['price']} TL" 
                      for f in st.session_state.found_flights]

    # Let the user pick a flight
    selected_index = st.radio("Select a flight to purchase:", 
                              options=list(range(len(flight_options))),
                              format_func=lambda i: flight_options[i])

    # 7. "Confirm Selection" button
    if st.button("Confirm Selection"):
        # Retrieve the actual flight dict
        chosen_flight = st.session_state.found_flights[selected_index]
        st.session_state.selected_flight = chosen_flight

        # 7A. We send a new user message to the LLM, 
        #     e.g., "I want to purchase flight TK103."
        msg = f"I want to purchase this flight: {chosen_flight}"
        st.session_state.messages.append({"role": "user", "content": msg})
        with st.chat_message("user"):
            st.write(msg)

        # 7B. Rebuild the formatted history including this new user message
        formatted_history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )
        # 7C. Agent run again
        response = st.session_state.agent.run(
            input=msg,
            chat_history=formatted_history
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)


if __name__ == "__main__":
    main()
