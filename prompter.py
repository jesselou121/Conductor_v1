import anthropic
import json
import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_prompt(file_name):
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_name, 'r', encoding=encoding) as file:
                return file.read().strip()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read {file_name} with any of the attempted encodings")

def run_tea_engine_prompts(product, feedstock):
    try:
        # Get API key from Streamlit secrets
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

        # Initialize messages list
        messages = []

        # System message
        system_message = "You are an expert chemical engineer specializing in bio-manufacturing processes. Your task is to design and describe processes for creating various bio-based products from different feedstocks. You have extensive knowledge of biochemical pathways, industrial biotechnology, and process engineering. Your descriptions should be technically accurate, detailed, and follow best practices in the field."

        # Process each prompt
        yield {"role": "system", "content": system_message}

        for i in range(1, 6):
            prompt_file = f"prompts/prompt{i}.txt"
            try:
                prompt_content = read_prompt(prompt_file)
            except ValueError as e:
                logger.error(f"Error reading prompt file {prompt_file}: {str(e)}")
                yield {"role": "error", "content": f"Error reading prompt file {prompt_file}. Please check the file encoding."}
                return

            # Replace placeholders in the prompt
            prompt_content = prompt_content.replace("{{PRODUCT}}", product).replace("{{FEEDSTOCK}}", feedstock)

            messages.append({"role": "user", "content": [{"type": "text", "text": prompt_content}]})
            yield {"role": "user", "content": prompt_content}

            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4000,
                temperature=0,
                system=system_message,
                messages=messages
            )

            assistant_message = response.content[0].text
            messages.append({"role": "assistant", "content": [{"type": "text", "text": response.content[0].text}]})
            yield {"role": "assistant", "content": assistant_message}

        final_response = response.content[0].text
        try:
            json_output = json.loads(final_response)
        except json.JSONDecodeError:
            logger.error("Final response is not a valid JSON")
            json_output = {"error": "Invalid JSON output", "raw_response": final_response}

        return json_output

    except Exception as e:
        logger.error(f"Error in run_tea_engine_prompts: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        return None

# Ensure the function is available for import
__all__ = ['run_tea_engine_prompts']