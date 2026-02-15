This project is a simple web-based AI-powered travel planner built with Streamlit. It allows users to input a city, their interests (comma-separated), and an optional custom request to generate a personalized one-day trip itinerary. The backend uses LangGraph for workflow orchestration, LangChain for prompt handling, and Groq's Llama 3.1 model for generating the itinerary via AI.
The app is designed to be lightweight, easy to deploy, and extensible. If you're returning to this project after a while, here's the quick essence:

Core Flow: User inputs → State management via LangGraph → LLM invocation → Display itinerary.
Why Built This Way: To demonstrate a basic agentic workflow with LangGraph in a user-friendly Streamlit UI, keeping inputs simple and outputs actionable.

Key Features

User Inputs: City, interests (e.g., "food, history, adventure"), and a custom request (defaults to "I want to plan a day trip").
AI Generation: Uses Groq's fast LLM to create a bulleted day trip itinerary based on inputs.
Validation: Checks for required fields (city and interests) before processing.
Spinner & Feedback: Shows loading spinner during generation and success message on completion.
Modular Design: LangGraph handles the stateful workflow, making it easy to add more nodes (e.g., for multi-day trips or recommendations).

Technologies Used

Frontend: Streamlit (for interactive web UI).
Backend Workflow: LangGraph (stateful graph for agent logic).
AI Integration: LangChain (prompt templates and messages), ChatGroq (LLM provider with Llama-3.1-8B model).
Environment Management: dotenv (for API keys).
Python Version: 3.10+ (compatible with all libraries).
Dependencies: Listed in requirements.txt (create one if missing: streamlit, langgraph, langchain-core, langchain-groq, python-dotenv).

Installation & Setup

Clone the Repository:textgit clone https://github.com/yourusername/ai-day-trip-planner.git
cd ai-day-trip-planner
Set Up Environment:
Install dependencies:textpip install -r requirements.txt
Create a .env file in the root directory and add your Groq API key:textGROQ_API_KEY=your_groq_api_key_here(Get your key from Groq Console.)

Run the App:textstreamlit run app.py
Open http://localhost:8501 in your browser.


Usage

Launch the app via Streamlit.
Enter the city (e.g., "Paris").
Enter interests as comma-separated values (e.g., "museums, food, sightseeing").
Optionally edit the request textarea.
Click "Generate Itinerary" → Wait for the AI to process → View the bulleted itinerary.

Example Output:

Morning: Visit the Eiffel Tower for panoramic views.
Afternoon: Explore the Louvre Museum.
Evening: Enjoy French cuisine at a local bistro.

If errors occur (e.g., API key missing), check the console for logs.
Project Structure
textai-day-trip-planner/
├── app.py              # Main Streamlit app script (UI + LangGraph integration)
├── requirements.txt    # List of Python dependencies
├── .env                # Environment variables (API keys) - gitignored
├── README.md           # This file
└── .gitignore          # Standard ignores for Python/Streamlit projects

app.py Breakdown:
Imports & Setup: Loads libraries, defines state, LLM, and prompt.
Graph Nodes: Only one node (create_itinerary) for simplicity – formats prompt, calls LLM, updates state.
Graph Building: Linear flow from START to itinerary creation.
Streamlit UI: Inputs, button, spinner, and markdown display.


Potential Improvements

Add more LangGraph nodes (e.g., for weather integration or multi-step planning).
Enhance UI with multiselect for interests or session state for multiple itineraries.
Error Handling: Add try-except for LLM calls.
Deployment: Host on Streamlit Cloud or Heroku.
