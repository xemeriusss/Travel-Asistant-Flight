# WITHOUT SIDEBAR

# # app.py
# import streamlit as st
# from agent import create_agent
# from callback import ToolOutputCatcher
# import ast

# def parse_flights(flights_str: str):
#     """
#     flights_str might be something like '[{...},{...}]'.
#     Parse into a list of dicts.
#     """
#     try:
#         data = ast.literal_eval(flights_str)
#         if isinstance(data, dict):
#             data = [data]
#         return data
#     except:
#         return []

# def main():
#     st.title("Travel Assistant")

#     if "agent" not in st.session_state:
#         st.session_state.agent = create_agent()
#         st.session_state.messages = []

#         st.session_state.outbound_flights = []
#         st.session_state.inbound_flights = []

#     # Display chat history
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # Chat input
#     user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
#     if user_input:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)

#         # Format chat history
#         formatted_history = "\n".join(
#             f"{m['role'].capitalize()}: {m['content']}" 
#             for m in st.session_state.messages
#         )

#         # Attach callback to catch flight search results
#         callback_handler = ToolOutputCatcher()

#         # Run the agent
#         response = st.session_state.agent.run(
#             input=user_input,
#             chat_history=formatted_history,
#             callbacks=[callback_handler]
#         )

#         # Add assistant response to chat
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

#         # # If the callback caught flight data, parse & store
#         # if callback_handler.search_flights_output:
#         #     parsed = parse_flights(callback_handler.search_flights_output)
#         #     st.session_state.found_flights = parsed

#         # Check how many times the search_flights_tool was called
#         outputs = callback_handler.search_flights_outputs
#         if outputs:
#             if len(outputs) == 1:
#                 # One-way or partial search
#                 st.session_state.outbound_flights = parse_flights(outputs[0])
#                 st.session_state.inbound_flights = []  # no inbound
#             elif len(outputs) == 2:
#                 # Round-trip
#                 st.session_state.outbound_flights = parse_flights(outputs[0])
#                 st.session_state.inbound_flights = parse_flights(outputs[1])
#             else:
#                 # Rarely, if there's more than 2 calls...
#                 # you might handle that differently or just store them all
#                 pass

#     st.divider()

#     # 8. Outbound flights
#     if st.session_state.outbound_flights:
#         st.write("### Outbound Flights")
#         outbound_options = [
#             f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
#             for f in st.session_state.outbound_flights
#         ]
#         chosen_outbound_idx = st.radio(
#             "Select Outbound:",
#             options=range(len(outbound_options)),
#             format_func=lambda i: outbound_options[i]
#         )
#         outbound_flight = st.session_state.outbound_flights[chosen_outbound_idx]

#     # 9. Inbound flights
#     if st.session_state.inbound_flights:
#         st.write("### Inbound Flights")
#         inbound_options = [
#             f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
#             for f in st.session_state.inbound_flights
#         ]
#         chosen_inbound_idx = st.radio(
#             "Select Inbound:",
#             options=range(len(inbound_options)),
#             format_func=lambda i: inbound_options[i]
#         )
#         inbound_flight = st.session_state.inbound_flights[chosen_inbound_idx]
#     else:
#         inbound_flight = None

#     # 10. Confirm Purchase button
#     if st.button("Confirm Purchase"):
#         if outbound_flight and inbound_flight:
#             user_msg = f"I choose outbound flight {outbound_flight} and inbound flight {inbound_flight}."
#         elif outbound_flight:
#             user_msg = f"I choose flight {outbound_flight}."  # one-way scenario
#         else:
#             user_msg = "I haven't picked any flight."

#         st.session_state.messages.append({"role": "user", "content": user_msg})
#         with st.chat_message("user"):
#             st.write(user_msg)

#         # Rerun agent
#         history_str = "\n".join(
#             f"{m['role'].capitalize()}: {m['content']}"
#             for m in st.session_state.messages
#         )
#         purchase_cb = ToolOutputCatcher()
#         purchase_response = st.session_state.agent.run(
#             input=user_msg,
#             chat_history=history_str,
#             callbacks=[purchase_cb]
#         )
#         st.session_state.messages.append({"role": "assistant", "content": purchase_response})
#         with st.chat_message("assistant"):
#             st.write(purchase_response)

# if __name__ == "__main__":
#     main()


############################################### WITH SIDEBAR ###############################################

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
    st.title("Travel Assistant")

    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
        st.session_state.messages = []

        st.session_state.outbound_flights = []
        st.session_state.inbound_flights = []

        st.session_state.current_step = "Topic Analysis"

        st.session_state.past_purchases = []

    # col1, col2 = st.columns([3, 2])

    # # ---- SIDEBAR CODE START ----
    # # A list of workflow steps in English
    # steps = ["Topic Analysis", "Information Gathering", "Flight Search", "Ticket Purchase"]

    # # Render the sidebar header
    # st.sidebar.title("Process Steps")

    # # Find index of current_step in the steps list
    # step_index = steps.index(st.session_state.current_step)

    # # Display each step with a checkmark if completed, bold if current
    # for i, step_name in enumerate(steps):
    #     if i < step_index:
    #         # A completed step
    #         st.sidebar.markdown(f"✅ **{step_name}**")
    #     elif i == step_index:
    #         # The current step
    #         st.sidebar.markdown(f"🔄 **{step_name}**")
    #     else:
    #         # Future steps
    #         st.sidebar.markdown(step_name)
    # # ---- SIDEBAR CODE END ----

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
    if user_input:

        if "buy" in user_input.lower() or "purchase" in user_input.lower():
            st.session_state.current_step = "Information Gathering"

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

        # # If the callback caught flight data, parse & store
        # if callback_handler.search_flights_output:
        #     parsed = parse_flights(callback_handler.search_flights_output)
        #     st.session_state.found_flights = parsed

        # Check how many times the search_flights_tool was called
        outputs = callback_handler.search_flights_outputs
        if outputs:
            if len(outputs) == 1:
                # One-way or partial search
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = []  # no inbound

                st.session_state.current_step = "Flight Search"

            elif len(outputs) == 2:
                # Round-trip
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = parse_flights(outputs[1])

                st.session_state.current_step = "Flight Search"

            else:
                # Rarely, if there's more than 2 calls...
                # you might handle that differently or just store them all
                pass

    st.divider()
           
    # 8. Outbound flights
    if st.session_state.outbound_flights:
        st.write("### Outbound Flights")
        outbound_options = [
            f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
            for f in st.session_state.outbound_flights
        ]
        chosen_outbound_idx = st.radio(
            "Select Outbound:",
            options=range(len(outbound_options)),
            format_func=lambda i: outbound_options[i]
        )
        outbound_flight = st.session_state.outbound_flights[chosen_outbound_idx]
    else:
        outbound_flight = None

    # 9. Inbound flights
    if st.session_state.inbound_flights:
        st.write("### Inbound Flights")
        inbound_options = [
            f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
            for f in st.session_state.inbound_flights
        ]
        chosen_inbound_idx = st.radio(
            "Select Inbound:",
            options=range(len(inbound_options)),
            format_func=lambda i: inbound_options[i]
        )
        inbound_flight = st.session_state.inbound_flights[chosen_inbound_idx]
    else:
        inbound_flight = None

    # st.divider()

    # 10. Confirm Purchase button
    if st.button("Confirm Purchase"):

        st.session_state.current_step = "Ticket Purchase"

        if outbound_flight and inbound_flight:
            user_msg = f"I choose outbound flight {outbound_flight} and inbound flight {inbound_flight}."

            st.session_state.past_purchases.append({
                "outbound": outbound_flight,
                "inbound": inbound_flight
            })

        elif outbound_flight:
            user_msg = f"I choose flight {outbound_flight}."  # one-way scenario

            st.session_state.past_purchases.append({
                "outbound": outbound_flight
            })
            
        else:
            user_msg = "I haven't picked any flight."

        st.session_state.messages.append({"role": "user", "content": user_msg})

        with st.chat_message("user"):
            # st.write(user_msg)
            if outbound_flight and inbound_flight:
                flight_details = f"""
                I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]} and  {inbound_flight["flight_code"]} operated by {inbound_flight["carrier"]}."""

                # Departure: {outbound_flight["departure_city"]} → {outbound_flight["arrival_city"]}
                # Date: {outbound_flight["departure_date"]}
                # Boarding Time: {outbound_flight["boarding_time"]}
                # Landing Time: {outbound_flight["landing_time"]}
                # Class: {outbound_flight["class"]}
                # Price: {outbound_flight["price"]} TRY
                # """

                st.write(flight_details)

            elif outbound_flight:
                flight_details = f"""
                I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]}."""

                # Departure: {inbound_flight["departure_city"]} → {inbound_flight["arrival_city"]}
                # Date: {inbound_flight["departure_date"]}
                # Boarding Time: {inbound_flight["boarding_time"]}
                # Landing Time: {inbound_flight["landing_time"]}
                # Class: {inbound_flight["class"]}
                # Price: {inbound_flight["price"]} TRY
                # """

                st.write(flight_details)

            else:
                st.write(user_msg)
            
        # Rerun agent
        history_str = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )
        purchase_cb = ToolOutputCatcher()
        purchase_response = st.session_state.agent.run(
            input=user_msg,
            chat_history=history_str,
            callbacks=[purchase_cb]
        )
        st.session_state.messages.append({"role": "assistant", "content": purchase_response})
        with st.chat_message("assistant"):
            st.write(purchase_response)

if __name__ == "__main__":
    main()


###################################### RADIO BUTTON INSIDE CHAT (error for nested) #################################

# import streamlit as st
# from agent import create_agent
# from callback import ToolOutputCatcher
# import ast

# def parse_flights(flights_str: str):
#     try:
#         data = ast.literal_eval(flights_str)
#         if isinstance(data, dict):
#             data = [data]
#         return data
#     except:
#         return []

# def main():
#     st.title("Travel Assistant with Minimal Prefix Update")

#     if "agent" not in st.session_state:
#         st.session_state.agent = create_agent()
#         st.session_state.messages = []
#         st.session_state.outbound_flights = []
#         st.session_state.inbound_flights = []

#     # 1. Display existing chat history
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # 2. Chat input
#     user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
#     if user_input:
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)

#         # Format chat history for the agent
#         formatted_history = "\n".join(
#             f"{m['role'].capitalize()}: {m['content']}"
#             for m in st.session_state.messages
#         )

#         # Capture flight tool outputs
#         callback_handler = ToolOutputCatcher()
#         response = st.session_state.agent.run(
#             input=user_input,
#             chat_history=formatted_history,
#             callbacks=[callback_handler]
#         )

#         # Agent's response
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

#         # If the agent called the search tool
#         outputs = callback_handler.search_flights_outputs
#         if outputs:
#             if len(outputs) == 1:
#                 # One-way
#                 st.session_state.outbound_flights = parse_flights(outputs[0])
#                 st.session_state.inbound_flights = []
#             elif len(outputs) == 2:
#                 # Round-trip
#                 st.session_state.outbound_flights = parse_flights(outputs[0])
#                 st.session_state.inbound_flights = parse_flights(outputs[1])
#             # if there's more calls, handle them as needed

#     # 3. Combine flight selection & purchase into one top-level chat message
#     if st.session_state.outbound_flights or st.session_state.inbound_flights:
#         with st.chat_message("assistant"):
#             # Outbound flights
#             outbound_flight = None
#             if st.session_state.outbound_flights:
#                 st.write("### Outbound Flights (Select One)")
#                 outbound_options = [
#                     f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
#                     for f in st.session_state.outbound_flights
#                 ]
#                 chosen_outbound_idx = st.radio(
#                     "Outbound Flight",
#                     options=range(len(outbound_options)),
#                     format_func=lambda i: outbound_options[i],
#                     key="chosen_outbound_idx"
#                 )
#                 outbound_flight = st.session_state.outbound_flights[chosen_outbound_idx]

#             # Inbound flights
#             inbound_flight = None
#             if st.session_state.inbound_flights:
#                 st.write("### Inbound Flights (Select One)")
#                 inbound_options = [
#                     f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']}"
#                     for f in st.session_state.inbound_flights
#                 ]
#                 chosen_inbound_idx = st.radio(
#                     "Inbound Flight",
#                     options=range(len(inbound_options)),
#                     format_func=lambda i: inbound_options[i],
#                     key="chosen_inbound_idx"
#                 )
#                 inbound_flight = st.session_state.inbound_flights[chosen_inbound_idx]

#             # Confirm Purchase Button
#             if st.button("Confirm Purchase"):
#                 if outbound_flight and inbound_flight:
#                     user_msg = f"I choose outbound flight {outbound_flight} and inbound flight {inbound_flight}."
#                 elif outbound_flight:
#                     user_msg = f"I choose flight {outbound_flight}."
#                 else:
#                     user_msg = "I haven't picked any flight."

#                 st.session_state.messages.append({"role": "user", "content": user_msg})
#                 with st.chat_message("user"):
#                     st.write(user_msg)

#                 history_str = "\n".join(
#                     f"{m['role'].capitalize()}: {m['content']}"
#                     for m in st.session_state.messages
#                 )
#                 purchase_cb = ToolOutputCatcher()
#                 purchase_response = st.session_state.agent.run(
#                     input=user_msg,
#                     chat_history=history_str,
#                     callbacks=[purchase_cb]
#                 )
#                 st.session_state.messages.append({"role": "assistant", "content": purchase_response})
#                 with st.chat_message("assistant"):
#                     st.write(purchase_response)

# if __name__ == "__main__":
#     main()

