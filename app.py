import streamlit as st
from agent import create_agent
from callback import ToolOutputCatcher
import ast

# Helper function to parse flight data
def parse_flights(flights_str: str):
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
        st.session_state.agent = create_agent() # Create the agent
        st.session_state.messages = [] # Chat history to store messages

        st.session_state.outbound_flights = [] # Store outbound flights
        st.session_state.inbound_flights = [] # Store inbound flights

        st.session_state.past_purchases = [] # Store past purchases

        # st.session_state.current_step = "Topic Analysis"

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
    if user_input:

        # if "buy" in user_input.lower() or "purchase" in user_input.lower():
        #     st.session_state.current_step = "Information Gathering"

        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Before the agent processes the input, the entire conversation history is formatted into a string.
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

        # Check how many times the search_flights_tool was called to seperate outbound and inbound flights
        outputs = callback_handler.search_flights_outputs

        if outputs:
            if len(outputs) == 1:
                # One-way or partial search
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = []  # no inbound

            elif len(outputs) == 2:
                # Round-trip
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = parse_flights(outputs[1])

            else:
                pass

    st.divider()
           
    # Ticket Selection and Purchase Section

    # Outbound flights
    if st.session_state.outbound_flights:
        st.write("### Outbound Flights")

        outbound_options = [
            f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']} - {f['class']}"
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

    # Inbound flights
    if st.session_state.inbound_flights:
        st.write("### Inbound Flights")

        inbound_options = [
            f"{f['flight_code']} - {f['price']} TL - {f['boarding_time']} - {f['landing_time']} - {f['class']}"
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

    # Confirm Purchase button
    if st.button("Confirm Purchase"):

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

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_msg})

        # Display user message
        with st.chat_message("user"):

            if outbound_flight and inbound_flight:
                flight_details = f"""
                I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]} and  {inbound_flight["flight_code"]} operated by {inbound_flight["carrier"]}."""

                st.write(flight_details)

            elif outbound_flight:
                flight_details = f"""
                I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]}."""

                st.write(flight_details)

            else:
                st.write(user_msg)
            
        # Format chat history to string
        history_str = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )

        # Attach callback to catch purchase results
        purchase_cb = ToolOutputCatcher()
        
        # Rerun the agent to process the purchase
        purchase_response = st.session_state.agent.run(
            input=user_msg,
            chat_history=history_str,
            callbacks=[purchase_cb]
        )

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": purchase_response})
        with st.chat_message("assistant"):
            st.write(purchase_response)

if __name__ == "__main__":
    main()


