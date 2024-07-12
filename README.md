TEA Generator and Visualizer
This Streamlit application allows users to generate process flows for bio-manufacturing processes and visualize Techno-Economic Analysis (TEA) results.
Features

Generate process flows by specifying a product and feedstock
Visualize TEA results from uploaded JSON files
Display flow tables and diagrams

Installation

Clone this repository:
Copygit clone https://github.com/yourusername/tea-streamlit-app.git
cd tea-streamlit-app

Create a virtual environment and activate it:
Copypython -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:
Copypip install -r requirements.txt

Set up your Anthropic API key:

Create a .streamlit/secrets.toml file in the project root
Add your API key to the file:
CopyANTHROPIC_API_KEY = "your-api-key-here"




Usage

Run the Streamlit app:
Copystreamlit run app.py

Open your web browser and go to the URL displayed in the terminal (usually http://localhost:8501)
Use the "Generate Process Flow" tab to create a new process flow:

Enter the product and feedstock
Click "Generate Process Flow"
Download the resulting JSON file


Use the "Visualize TEA" tab to analyze an existing process flow:

Upload a JSON file
View the flow table and diagram



Project Structure

app.py: Main Streamlit application
tea_engine.py: TEA calculation and visualization functions
prompter.py: LLM prompting functionality
prompts/: Directory containing prompt templates