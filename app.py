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
    
    # Initialize session state
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent() # Create the agent
        st.session_state.messages = [] # Chat history to store messages
        st.session_state.outbound_flights = [] # Store outbound flights
        st.session_state.inbound_flights = [] # Store inbound flights
        st.session_state.past_purchases = [] # Store past purchases
        st.session_state.selected_outbound = None
        st.session_state.selected_inbound = None
        st.session_state.process_steps = []  # Track agent process steps
        st.session_state.current_step = -1  # Current step in the process
        st.session_state.purchase_completed = False  # Flag for purchase completion
    
    # Create sidebar for process tracking
    with st.sidebar:
        st.header("Process Tracking")
        
        if st.session_state.process_steps:
            for i, step in enumerate(st.session_state.process_steps):
                if i == st.session_state.current_step:
                    st.markdown(f"### → **{step}** (Current)")
                else:
                    st.markdown(f"### {step}")
        else:
            st.info("Start a conversation to see process steps")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg.get("display_content", msg["content"]))

    # Chat input
    user_input = st.chat_input("Ask about flights or say 'I want to buy a ticket'...")
    
    if user_input:
        # Reset purchase completion flag on new interaction
        st.session_state.purchase_completed = False
        
        # Clear previous flight selections when starting a new search
        if "buy" in user_input.lower() and "ticket" in user_input.lower():
            st.session_state.outbound_flights = []
            st.session_state.inbound_flights = []
            st.session_state.selected_outbound = None
            st.session_state.selected_inbound = None
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Update process tracking
        st.session_state.process_steps = ["Information Gathering", "Processing Request"]
        st.session_state.current_step = 0
        
        # Format conversation history for the agent
        formatted_history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" 
            for m in st.session_state.messages
        )

        # Attach callback to catch flight search results
        callback_handler = ToolOutputCatcher()
        
        # Update process step
        # st.session_state.current_step = 1
        
        # Run the agent to get a response
        response = st.session_state.agent.run(
            input=user_input,
            chat_history=formatted_history,
            callbacks=[callback_handler]
        )
        
        # Update process step
        st.session_state.current_step = 1
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

        # Get flight search outputs from the callback handler
        outputs = callback_handler.search_flights_outputs

        if outputs:
            # Update process steps for flight search
            st.session_state.process_steps.append("Searching Flights")
            st.session_state.current_step = 2

            print("Outputs:", outputs)
            
            if len(outputs) == 1:
                # One-way or partial search
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = []  # no inbound
                st.session_state.selected_outbound = None
                st.session_state.selected_inbound = None
            elif len(outputs) == 2:
                # Round-trip
                st.session_state.outbound_flights = parse_flights(outputs[0])
                st.session_state.inbound_flights = parse_flights(outputs[1])
                st.session_state.selected_outbound = None
                st.session_state.selected_inbound = None
            
            # Add flight display step
            st.session_state.process_steps.append("Displaying Flight Options")
            st.session_state.current_step = 3

    # Display flight selection section if there are flights and purchase is not completed
    if (st.session_state.outbound_flights or st.session_state.inbound_flights) and not st.session_state.purchase_completed:
        st.divider()
        st.header("Flight Selection", anchor=False)
        
        # If both outbound and inbound flights are available, show tabs
        if st.session_state.inbound_flights:
            tab1, tab2 = st.tabs(["Outbound Flights", "Inbound Flights"])
        else:
            tab1 = st.tabs(["Outbound Flights"])[0]
            
        # Display outbound flights
        with tab1:
            if st.session_state.outbound_flights:
                st.subheader("Select Your Outbound Flight")
                
                # Create columns for flight cards
                cols = st.columns(1)
                
                for i, flight in enumerate(st.session_state.outbound_flights):
                    with cols[i % 1]: 
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**{flight['flight_code']}** - {flight['carrier']}")
                                st.markdown(f"**{flight['boarding_time']} → {flight['landing_time']}**")
                                st.markdown(f"Class: {flight['class']}")
                            
                            with col2:
                                st.markdown(f"### {flight['price']} TL")
                                is_selected = st.session_state.selected_outbound == i
                                if st.button("Select" if not is_selected else "Selected ✓", 
                                            key=f"out_{i}", 
                                            type="primary" if is_selected else "secondary"):
                                    st.session_state.selected_outbound = i
                                    st.rerun() # Rerun to update selection
        
        # Display inbound flights if available
        if st.session_state.inbound_flights:
            with tab2:
                st.subheader("Select Your Inbound Flight")
                
                # Create columns for flight cards
                cols = st.columns(1)
                
                for i, flight in enumerate(st.session_state.inbound_flights):
                    with cols[i % 1]: 
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**{flight['flight_code']}** - {flight['carrier']}")
                                st.markdown(f"**{flight['boarding_time']} → {flight['landing_time']}**")
                                st.markdown(f"Class: {flight['class']}")
                            
                            with col2:
                                st.markdown(f"### {flight['price']} TL")
                                is_selected = st.session_state.selected_inbound == i
                                if st.button("Select" if not is_selected else "Selected ✓", 
                                            key=f"in_{i}", 
                                            type="primary" if is_selected else "secondary"):
                                    st.session_state.selected_inbound = i
                                    st.rerun() # Rerun to update selection

        # Display order summary if flights are selected
        if st.session_state.selected_outbound is not None or st.session_state.selected_inbound is not None:
            st.divider()
            st.subheader("Order Summary")
            
            total_price = 0
            
            if st.session_state.selected_outbound is not None:
                outbound_flight = st.session_state.outbound_flights[st.session_state.selected_outbound]
                st.markdown(f"**Outbound Flight:** {outbound_flight['flight_code']} - {outbound_flight['carrier']}")
                st.markdown(f"**Date:** {outbound_flight['boarding_time']} → {outbound_flight['landing_time']}")
                st.markdown(f"**Class:** {outbound_flight['class']}")
                st.markdown(f"**Price:** {outbound_flight['price']} TL")
                total_price += float(outbound_flight['price']) # add price to total
            
            if st.session_state.selected_inbound is not None:
                inbound_flight = st.session_state.inbound_flights[st.session_state.selected_inbound]
                st.markdown(f"**Inbound Flight:** {inbound_flight['flight_code']} - {inbound_flight['carrier']}")
                st.markdown(f"**Date:** {inbound_flight['boarding_time']} → {inbound_flight['landing_time']}")
                st.markdown(f"**Class:** {inbound_flight['class']}")
                st.markdown(f"**Price:** {inbound_flight['price']} TL")
                total_price += float(inbound_flight['price'])
            
            st.markdown(f"### Total Price: {total_price} TL")
            
            # Confirm Purchase button
            if st.button("Confirm Purchase", type="primary", use_container_width=True):
                outbound_flight = None
                inbound_flight = None
                
                if st.session_state.selected_outbound is not None:
                    outbound_flight = st.session_state.outbound_flights[st.session_state.selected_outbound] # get selected outbound flight
                
                if st.session_state.selected_inbound is not None:
                    inbound_flight = st.session_state.inbound_flights[st.session_state.selected_inbound] # get selected inbound flight
                
                # Create the raw message for the agent 
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
                
                # Create the display message after selection
                if outbound_flight and inbound_flight:
                    display_msg = f"""
                    I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]} and {inbound_flight["flight_code"]} operated by {inbound_flight["carrier"]}."""

                elif outbound_flight:
                    display_msg = f"""
                    I choose flight {outbound_flight["flight_code"]} operated by {outbound_flight["carrier"]}."""

                else:
                    display_msg = "I haven't picked any flight."
                
                # Add user message to chat history with both content versions
                st.session_state.messages.append({
                    "role": "user", 
                    "content": user_msg,
                    "display_content": display_msg
                })
                
                # Display user message in chat
                with st.chat_message("user"):
                    st.write(display_msg)
                
                # Update process steps for purchase
                st.session_state.process_steps.append("Processing Purchase")
                st.session_state.current_step = 4
                
                # Format chat history to string for agent
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
                
                # Add completion step
                st.session_state.process_steps.append("Purchase Complete")
                st.session_state.current_step = 5
                
                # Mark purchase as completed to hide flight selection section
                st.session_state.purchase_completed = True
                
                # Reset selections
                st.session_state.selected_outbound = None
                st.session_state.selected_inbound = None
                st.rerun() # Rerun to hide flight selection section

if __name__ == "__main__":
    main()