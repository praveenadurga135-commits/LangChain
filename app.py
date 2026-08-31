import os
from dotenv import load_dotenv
import streamlit as st

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

load_dotenv()

st.set_page_config(
    page_title="LangChain Trip Planner",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background: #0f172a; color: #e5e7eb; }
.block-container { padding-top: 1.5rem; max-width: 1200px; }
.hero {
    background: linear-gradient(135deg, #111827, #020617);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 20px;
}
.hero h1 { font-size: 38px; font-weight: 800; color: #ffffff; margin-bottom: 8px; }
.hero p { color: #cbd5e1; font-size: 16px; }
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    font-weight: 700;
    margin-bottom: 10px;
}
.card {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 16px;
}
.stButton button {
    border-radius: 14px;
    background: #38bdf8;
    color: #020617;
    font-weight: 800;
    border: none;
    padding: 0.65rem 1rem;
}
.stButton button:hover {
    background: #0ea5e9;
    color: #020617;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="badge">AI School of India · LangChain Prompt Templates Project</div>
    <h1>✈️ AI Trip Planner using LangChain</h1>
    <p>Learn Single-turn PromptTemplate, ChatPromptTemplate, Dynamic Variables, and Multi-turn Conversation using one practical travel planning app.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Model Settings")

    provider = st.radio(
        "Choose Provider",
        ["Groq API", "Ollama Local"],
        index=0,
        help="Groq needs API key. Ollama runs locally."
    )

    groq_model = st.selectbox(
        "Groq Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-8b-8192","openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "qwen/qwen3.6-27b"
        ],
        index=0
    )

    ollama_model = st.selectbox(
        "Ollama Model",
        [
            "qwen2.5:3b",
            "llama3.2:1b",
            "llama3.2",
            "mistral"
        ],
        index=0
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)

    st.markdown("---")
    st.markdown("### What you will teach")
    st.markdown("""
    1. Single-turn PromptTemplate  
    2. ChatPromptTemplate  
    3. Dynamic Variables  
    4. Multi-turn with Memory  
    """)

def get_llm():
    if provider == "Groq API":
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.error("GROQ_API_KEY not found. Add it in your .env file.")
            st.stop()

        return ChatGroq(
            groq_api_key=api_key,
            model=groq_model,
            temperature=temperature
        )

    return ChatOllama(
        model=ollama_model,
        temperature=temperature
    )
st.markdown("## 🧳 Trip Details")

c1, c2, c3 = st.columns(3)

with c1:
    destination = st.text_input("Destination", value="Goa")
    days = st.number_input("Number of Days", min_value=1, max_value=30, value=3)

with c2:
    budget = st.selectbox("Budget", ["Low", "Medium", "Premium"], index=1)
    traveller_type = st.selectbox(
        "Traveller Type",
        ["Solo", "Couple", "Family", "Friends", "Students"],
        index=2
    )

with c3:
    interests = st.multiselect(
        "Interests",
        ["Beaches", "Food", "Adventure", "History", "Shopping", "Nature", "Temples", "Nightlife"],
        default=["Beaches", "Food", "Nature"]
    )
    language = st.selectbox("Output Language", ["English", "Telugu", "Tenglish"], index=0)

interests_text = ", ".join(interests)

tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Single-turn PromptTemplate",
    "2️⃣ ChatPromptTemplate",
    "3️⃣ Dynamic Variables",
    "4️⃣ Multi-turn Trip Chat"
])

with tab1:
    st.markdown("### 1️⃣ Single-turn PromptTemplate")
    st.markdown("""
    <div class="card">
    <b>Concept:</b> One input goes into a reusable prompt template, model generates one response.
    <br><br>
    <b>Flow:</b> User Inputs → PromptTemplate → LLM → Output
    </div>
    """, unsafe_allow_html=True)

    st.code("""
prompt = PromptTemplate.from_template(
    "Create a {days}-day trip plan for {destination}..."
)

chain = prompt | llm | StrOutputParser()
result = chain.invoke({...})
""", language="python")

    if st.button("Generate Single-turn Trip Plan"):
        llm = get_llm()
        parser = StrOutputParser()

        prompt = PromptTemplate.from_template("""
Create a {days}-day travel itinerary for {destination}.

Traveller type: {traveller_type}
Budget: {budget}
Interests: {interests}
Output language: {language}

Give:
1. Short overview
2. Day-wise plan
3. Food suggestions
4. Estimated budget tips
5. Travel tips

Keep it practical and beginner-friendly.
""")

        chain = prompt | llm | parser
        result = chain.invoke({
            "destination": destination,
            "days": days,
            "traveller_type": traveller_type,
            "budget": budget,
            "interests": interests_text,
            "language": language
        })
        st.markdown("### ✅ Output")
        st.write(result)

with tab2:
    st.markdown("### 2️⃣ ChatPromptTemplate")
    st.markdown("""
    <div class="card">
    <b>Concept:</b> ChatPromptTemplate separates System message and Human message.
    <br><br>
    <b>System:</b> Sets assistant role/personality.  
    <br>
    <b>Human:</b> Actual user task.
    </div>
    """, unsafe_allow_html=True)

    persona = st.selectbox(
        "Choose Travel Planner Persona",
        [
            "Friendly Telugu travel guide",
            "Budget travel expert",
            "Luxury travel consultant",
            "Family vacation planner",
            "Adventure trip expert"
        ],
        index=0
    )

    st.code("""
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}."),
    ("human", "Plan a trip to {destination}...")
])
""", language="python")

    if st.button("Generate Using ChatPromptTemplate"):
        llm = get_llm()
        parser = StrOutputParser()

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a {persona}. Give practical, safe, realistic and well-structured travel plans."
            ),
            (
                "human",
                """
Plan a {days}-day trip to {destination}.

Traveller type: {traveller_type}
Budget: {budget}
Interests: {interests}
Output language: {language}

Make the plan clear and useful.
"""
            )
        ])

        chain = prompt | llm | parser
        result = chain.invoke({
            "persona": persona,
            "destination": destination,
            "days": days,
            "traveller_type": traveller_type,
            "budget": budget,
            "interests": interests_text,
            "language": language
        })

        st.markdown("### ✅ Output")
        st.write(result)

with tab3:
    st.markdown("### 3️⃣ Dynamic Variables")
    st.markdown("""
    <div class="card">
    <b>Concept:</b> Dynamic variables are placeholders like <code>{destination}</code>, <code>{days}</code>, <code>{budget}</code>.
    <br><br>
    Same prompt can generate different plans by changing inputs.
    </div>
    """, unsafe_allow_html=True)

    food_preference = st.selectbox(
        "Food Preference",
        ["Vegetarian", "Non-Vegetarian", "Vegan", "Local Food", "No Preference"],
        index=3
    )

    travel_style = st.selectbox(
        "Travel Style",
        ["Relaxed", "Packed Schedule", "Balanced", "Photography Focused", "Kids Friendly"],
        index=2
    )

    avoid = st.text_input("Things to Avoid", value="too much walking, very expensive restaurants")

    st.code("""
Dynamic Variables:
{destination}, {days}, {budget}, {interests}, {food_preference}, {travel_style}, {avoid}
""", language="text")

    if st.button("Generate Plan with Dynamic Variables"):
        llm = get_llm()
        parser = StrOutputParser()

        prompt = PromptTemplate.from_template("""
You are an expert travel planner.

Create a personalized {days}-day trip plan.

Destination: {destination}
Traveller type: {traveller_type}
Budget: {budget}
Interests: {interests}
Food preference: {food_preference}
Travel style: {travel_style}
Things to avoid: {avoid}
Output language: {language}

Output format:
- Trip summary
- Day-wise itinerary
- Food recommendations
- Places to avoid / be careful
- Budget tips
- Final checklist
""")

        chain = prompt | llm | parser
        result = chain.invoke({
            "destination": destination,
            "days": days,
            "traveller_type": traveller_type,
            "budget": budget,
            "interests": interests_text,
            "food_preference": food_preference,
            "travel_style": travel_style,
            "avoid": avoid,
            "language": language
        })

        st.markdown("### ✅ Output")
        st.write(result)

with tab4:
    st.markdown("### 4️⃣ Multi-turn Trip Chat")
    st.markdown("""
    <div class="card">
    <b>Concept:</b> Multi-turn means the AI remembers previous messages in the current session.
    <br><br>
    <b>Flow:</b> Chat History + New Question → Prompt → LLM → Answer
    </div>
    """, unsafe_allow_html=True)

    if "trip_chat_history" not in st.session_state:
        st.session_state.trip_chat_history = []

    if st.button("Clear Multi-turn Chat"):
        st.session_state.trip_chat_history = []
        st.rerun()

    for msg in st.session_state.trip_chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    user_question = st.chat_input("Ask follow-up: Can you add beaches? Make it cheaper? Add kids-friendly places?")

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)

        llm = get_llm()
        parser = StrOutputParser()

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
You are a helpful AI trip planning assistant.
You remember the current conversation history and answer follow-up questions.
If the user asks to modify the trip, update the plan clearly.
Respond in {language}.
"""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

        chain = prompt | llm | parser
        result = chain.invoke({
            "language": language,
            "chat_history": st.session_state.trip_chat_history,
            "question": user_question
        })

        st.session_state.trip_chat_history.append(HumanMessage(content=user_question))
        st.session_state.trip_chat_history.append(AIMessage(content=result))

        with st.chat_message("assistant"):
            st.write(result)

