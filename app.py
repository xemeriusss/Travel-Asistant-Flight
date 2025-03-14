# # app.py
# import streamlit as st
# from agent import create_agent
# from callback import ToolOutputCatcher
# import ast

# def parse_flights_from_tool_output(tool_output):
#     """
#     tool_output is the string returned by 'search_flights_tool', e.g. "[{...}, {...}]"
#     Convert it into a list of flight dicts.
#     """
#     try:
#         data = ast.literal_eval(tool_output)
#         if isinstance(data, dict):
#             data = [data]
#         return data
#     except:
#         return []

# def main():
#     st.title("Option A: Use Callbacks to Track Tool Outputs")

#     if "agent" not in st.session_state:
#         st.session_state.agent = create_agent()
#         st.session_state.messages = []
#         # Will store the flights from the last search call
#         st.session_state.found_flights = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # Get user input
#     user_input = st.chat_input("Ask about flights... (e.g. 'Find flights from Istanbul,Ankara')")
#     if user_input:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)

#         # Prepare chat history
#         formatted_history = "\n".join(
#             f"{m['role'].capitalize()}: {m['content']}"
#             for m in st.session_state.messages
#         )

#         # 1. Create our callback to catch the flight search output
#         callback_handler = ToolOutputCatcher()

#         # 2. Run the agent, passing the callback
#         response = st.session_state.agent.run(
#             input=user_input,
#             chat_history=formatted_history,
#             callbacks=[callback_handler]
#         )

#         # 3. Add assistant reply to messages
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

#         # 4. Check if the callback caught an output from 'search_flights_tool'
#         if callback_handler.search_flights_output:
#             # Parse flights
#             flights_data = parse_flights_from_tool_output(callback_handler.search_flights_output)
#             st.session_state.found_flights = flights_data

#     st.divider()

#     # If we have flights, let user select one
#     if st.session_state.found_flights:
#         st.write("### Select a Flight to Purchase")
#         flight_options = [
#             f"{f['flight_code']} - {f['carrier']} - {f['price']} TL - {f['class']}"
#             for f in st.session_state.found_flights
#         ]
#         selected_index = st.radio(
#             "Which flight?",
#             options=list(range(len(flight_options))),
#             format_func=lambda i: flight_options[i]
#         )

#         # "Confirm Selection" triggers the actual purchase request
#         if st.button("Confirm Selection"):
#             chosen_flight = st.session_state.found_flights[selected_index]
#             # Build a user message for purchase
#             purchase_msg = f"I want to purchase this flight: {chosen_flight}."

#             st.session_state.messages.append({"role": "user", "content": purchase_msg})
#             with st.chat_message("user"):
#                 st.write(purchase_msg)

#             # Re-run agent with updated conversation
#             formatted_history = "\n".join(
#                 f"{m['role'].capitalize()}: {m['content']}"
#                 for m in st.session_state.messages
#             )

#             purchase_callback = ToolOutputCatcher()
#             purchase_response = st.session_state.agent.run(
#                 input=purchase_msg,
#                 chat_history=formatted_history,
#                 callbacks=[purchase_callback]
#             )
#             st.session_state.messages.append({"role": "assistant", "content": purchase_response})
#             with st.chat_message("assistant"):
#                 st.write(purchase_response)

#     else:
#         st.write("No flights found yet. Ask the assistant to search for flights first.")

# if __name__ == "__main__":
#     main()




# app.py
import streamlit as st
from agent import create_agent
from callback import ToolOutputCatcher
import ast

def parse_flights(flights_str: str):
    """
    flights_str might be something like '[{...},{...}]'.
    Parse into a list of dicts.
    """
    try:
        data = ast.literal_eval(flights_str)
        if isinstance(data, dict):
            data = [data]
        return data
    except:
        return []

def main():
    st.title("Travel Assistant with Minimal Prefix Update")

    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
        st.session_state.messages = []
        st.session_state.found_flights = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Format chat history
        formatted_history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" 
            for m in st.session_state.messages
        )

        # Attach callback to catch flight search results
        callback_handler = ToolOutputCatcher()

        # Run the agent
        response = st.session_state.agent.run(
            input=user_input,
            chat_history=formatted_history,
            callbacks=[callback_handler]
        )

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

        # If the callback caught flight data, parse & store
        if callback_handler.search_flights_output:
            parsed = parse_flights(callback_handler.search_flights_output)
            st.session_state.found_flights = parsed

    st.divider()

    # Show flights if any
    if st.session_state.found_flights:
        st.write("### Available Flights")
        flight_options = [
            f"{f['flight_code']} - {f['carrier']} - {f['price']} TL - {f['class']}"
            for f in st.session_state.found_flights
        ]
        selected_index = st.radio(
            "Pick a flight to purchase:",
            options=list(range(len(flight_options))),
            format_func=lambda i: flight_options[i],
        )

        if st.button("Confirm Purchase"):
            chosen_flight = st.session_state.found_flights[selected_index]
            # Send a new user message: "I want flight X"
            user_msg = f"I choose flight {chosen_flight}."

            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.chat_message("user"):
                st.write(user_msg)

            # Agent run again
            purchase_callback = ToolOutputCatcher()
            formatted_history = "\n".join(
                f"{m['role'].capitalize()}: {m['content']}" 
                for m in st.session_state.messages
            )
            purchase_response = st.session_state.agent.run(
                input=user_msg,
                chat_history=formatted_history,
                callbacks=[purchase_callback]
            )
            st.session_state.messages.append({"role": "assistant", "content": purchase_response})
            with st.chat_message("assistant"):
                st.write(purchase_response)

    else:
        st.write("No flights currently listed. Ask the assistant for a route first.")

if __name__ == "__main__":
    main()

