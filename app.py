import streamlit as st
import json
import io
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import functions from other modules
try:
    from prompter import run_tea_engine_prompts
    from tea_engine import calculate_flows, generate_flow_table, visualize_flow_diagram
except ImportError as e:
    logger.error(f"Error importing modules: {str(e)}")
    st.error(f"Failed to import required modules. Error: {str(e)}")

st.set_page_config(page_title="TEA Generator and Visualizer", layout="wide")

# Custom CSS for chat-like interface
st.markdown("""
<style>
    .user-message {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .assistant-message {
        background-color: #E0E0E0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

st.title("TEA Generator and Visualizer")

tab1, tab2 = st.tabs(["Generate Process Flow", "Visualize TEA"])

with tab1:
    st.header("Generate Process Flow")
    product = st.text_input("Enter the product:")
    feedstock = st.text_input("Enter the feedstock:")
    
    if st.button("Generate Process Flow"):
        if product and feedstock:
            try:
                json_output = None
                message_container = st.empty()
                messages = []

                for message in run_tea_engine_prompts(product, feedstock):
                    if message['role'] == 'json_output':
                        json_output = message['content']
                    else:
                        messages.append(message)
                        with message_container.container():
                            for msg in messages:
                                if msg['role'] == 'user':
                                    st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
                                elif msg['role'] == 'assistant':
                                    st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)
                                elif msg['role'] == 'system':
                                    st.info(msg['content'])
                                elif msg['role'] == 'error':
                                    st.error(msg['content'])

                if json_output:
                    st.json(json_output)
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(json_output, indent=2),
                        file_name=f"{product}_from_{feedstock}.json",
                        mime="application/json"
                    )
            except Exception as e:
                logger.error(f"Error generating process flow: {str(e)}")
                st.error(f"An error occurred while generating the process flow: {str(e)}")
        else:
            st.warning("Please enter both product and feedstock.")

with tab2:
    st.header("Visualize TEA")
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    
    if uploaded_file is not None:
        try:
            process_flow = json.load(uploaded_file)
            G, flows = calculate_flows(process_flow)
            
            st.subheader("Flow Table")
            st.text(generate_flow_table(process_flow, flows))
            
            st.subheader("Flow Diagram")
            fig, ax = plt.subplots(figsize=(12, 8))
            visualize_flow_diagram(G, flows, process_flow, ax)
            st.pyplot(fig)
        except Exception as e:
            logger.error(f"Error visualizing TEA: {str(e)}")
            st.error(f"An error occurred while visualizing the TEA: {str(e)}")