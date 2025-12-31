LLM_Council

LLM_Council is a Python project that runs a council of large language models (LLMs) to answer a user’s query by combining diverse model responses into a final consensus result. The system sends a prompt to multiple LLMs, collects their outputs, has them review and rank each other, and then uses a designated model to synthesize the final answer.

Features

Sends the same user prompt to multiple LLM providers

Models review and rank each other’s responses

A designated “chairman” model synthesizes the final answer

Uses OpenRouter to integrate with multiple model APIs

Includes an interactive interface (e.g., with Streamlit)

Repository Structure

streamlit_app.py – Frontend web interface for user input and display

council.py – Core logic for managing the model council and consensus

openrouter.py – OpenRouter API integration for multiple model calls

config.py – Configuration file for defining models and API settings

requirements.txt – Python dependencies

Requirements

Python 3.8 or higher

An OpenRouter API key

Setup and Installation

Clone the repository

git clone https://github.com/Fahadumergithub/LLM_council.git
cd LLM_council


Create a Python virtual environment and activate it

python -m venv venv
source venv/bin/activate


Install the dependencies

pip install -r requirements.txt


Configure your API key
Create a .env file in the project root and add:

OPENROUTER_API_KEY=your_openrouter_api_key

Usage

To start the interactive app:

streamlit run streamlit_app.py


Open the local URL shown in your browser. Enter a prompt and view the council’s collective answer.

How It Works

First Opinions
The prompt is sent to all configured LLMs independently.

Peer Review
Each model reviews other models’ responses and ranks them.

Final Answer
A designated chairman model synthesizes a final answer based on collective responses and rankings.

This multi-stage process helps produce answers informed by multiple perspectives. 
GitHub

Configuration

Edit config.py to customize the council:

Update the list of model identifiers to include the models you want

Set the chairman model for final answer synthesis

Tune other parameters such as temperature or output limits

Contributing

Contributions are welcome. You can:

Add new models or providers

Improve review or ranking logic

Enhance the interface

Add test cases and documentation

Please open an issue before submitting major changes.

License

Add your preferred license here and include a LICENSE file in the repository.
