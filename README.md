#  AI Code Assistant

A "Project-Aware" developer tool built with Python, Streamlit, and Google's Gemini 2.5 AI. 

Unlike standard AI chatbots that only see small snippets of code, this tool allows you to upload multiple project files and error screenshots into its memory. It uses this massive context window to help you debug complex, multi-file issues natively within a built-in code editor.

##  Features

* **Project Memory (Context Window):** Upload multiple `.py`, `.js`, `.txt`, or other text files to give the AI a complete understanding of your codebase.
* **Multimodal "Eyes":** Upload screenshots of error logs, terminal outputs, or architecture diagrams alongside your code.
* **Live Scratchpad:** An integrated code editor (powered by Streamlit-Ace) to paste and edit the specific functions you are actively working on.
* **Smart Chat Interface:** Ask questions about your project, and the AI will answer using the combined context of your files, images, and scratchpad.

##  Tech Stack

* **Frontend & Engine:** [Streamlit](https://streamlit.io/) (Pure Python UI framework)
* **Code Editor:** streamlit-ace
* **AI Model:** Google gemini-2.5-flash (via the google-genai SDK)
* **Image Processing:** Pillow (PIL)

##  Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites
* Python 3.8 or higher installed.
* A free API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Installation

Clone this repository or create a new project folder, then navigate into it using your terminal:

bash


mkdir ai-code-assistant
cd ai-code-assistant

Create and activate a virtual environment (recommended):

Bash

 Windows
python -m venv venv
venv\Scripts\activate

 Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install the required dependencies:

Bash
pip install streamlit streamlit-ace pillow google-genai python-dotenv
(Note: Be sure to install google-genai, not the deprecated google-generativeai library).

### 3. Configuration
Create a file named .env in the root of your project directory. Add your Google Gemini API key to this file:

Code snippet


GEMINI_API_KEY=your_actual_api_key_here


### 4. Running the App
Start the Streamlit development server by running:

Bash


streamlit run app.py
The application will automatically open in your default web browser at http://localhost:8501.


### Usage Guide
Upload Context: Open the sidebar and drop in your project files (e.g., schema.sql, main.py, utils.py).

Add Visuals (Optional): Drop a screenshot of a terminal error into the image uploader.

Edit Code: Paste the specific block of code you are trying to fix into the "Live Scratchpad" on the left side of the screen.

Chat: Ask the AI a question like, "Why is the code in my scratchpad failing based on the database schema in my uploaded files and the error in the screenshot?"
