import os
import streamlit as st
from typing import TypedDict, Annotated, List, Union

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# ---------------------------
# ENV
# ---------------------------
load_dotenv()

# ---------------------------
# STATE
# ---------------------------
class PlannerState(TypedDict):
    messages: Annotated[
        List[BaseMessage],
        add_messages,
        "Messages in the convo"
    ]
    city: str
    interests: List[str]
    itinerary: str

# ---------------------------
# LLM
# ---------------------------
llm = ChatGroq(
    temperature=0.5,
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ---------------------------
# PROMPT
# ---------------------------
itinerary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful travel assistant. "
        "Create a day trip itinerary for {city} based on the user's interests: {interests}. "
        "Provide a brief, bulleted itinerary."
    ),
    ("human", "Create an itinerary for my day trip"),
])

# ---------------------------
# GRAPH NODES
# ---------------------------
def create_itinerary(state: PlannerState) -> PlannerState:
    formatted_prompt = itinerary_prompt.format_messages(
        city=state["city"],
        interests=", ".join(state["interests"])
    )
    response = llm.invoke(formatted_prompt)

    return {
        **state,
        "messages": [AIMessage(content=response.content)],
        "itinerary": response.content
    }

# ---------------------------
# BUILD GRAPH
# ---------------------------
workflow = StateGraph(PlannerState)
workflow.add_node("create_itinerary", create_itinerary)
workflow.add_edge(START, "create_itinerary")
workflow.add_edge("create_itinerary", END)

app_graph = workflow.compile()

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("🧳 AI Day Trip Planner")

st.write("Plan a personalized one-day trip using AI ✨")

city = st.text_input("📍 Enter city")
interests = st.text_input("🎯 Enter interests (comma-separated)")
user_request = st.text_area(
    "📝 What do you want?",
    value="I want to plan a day trip"
)

if st.button("🚀 Generate Itinerary"):
    if not city or not interests:
        st.warning("Please enter both city and interests.")
    else:
        with st.spinner("Creating your itinerary..."):
            initial_state = {
                "messages": [HumanMessage(content=user_request)],
                "city": city.strip(),
                "interests": [i.strip() for i in interests.split(",")],
                "itinerary": "",
            }

            final_state = app_graph.invoke(initial_state)

            st.success("Your itinerary is ready!")
            st.markdown("### 📅 Day Trip Itinerary")
            st.markdown(final_state["itinerary"])