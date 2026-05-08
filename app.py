import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

st.set_page_config(
    page_title="Conversational Chatbot", 
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    :root {
        --primary-color: #dc143c;
        --secondary-color: #c41e3a;
        --background: #ffe6e6;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #dc143c 0%, #c41e3a 100%);
        min-height: 100vh;
    }
    
    .stChatMessage {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 0.8rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #dc143c 0%, #c41e3a 100%);
        color: white;
        margin-left: 20%;
        margin-bottom: 0.6rem;
        border-radius: 18px;
        padding: 1rem 1.5rem;
    }
    
    .bot-message {
        background: #fff5f5;
        color: #262730;
        margin-right: 20%;
        margin-bottom: 0.6rem;
        border-radius: 18px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #dc143c;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .chat-header h1 {
        font-size: 3em;
        margin: 0;
        font-weight: 900;
    }
    
    .chat-header p {
        font-size: 1.1em;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1.5rem;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 100;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #dc143c 0%, #c41e3a 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(220, 20, 60, 0.4);
    }
    
    .stTextInput input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        border: 2px solid #dc143c;
    }
    
    .stTextInput input:focus {
        border-color: #c41e3a;
        box-shadow: 0 0 0 0.2rem rgba(220, 20, 60, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Header with styling
st.markdown("""
    <div class="chat-header">
        <h1>🇬🇧 British Chat Mate</h1>
        <p>Blimey! Having a proper chinwag with some British flair!</p>
    </div>
""", unsafe_allow_html=True)

google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
requested_model = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

if not google_api_key:
    st.error("GOOGLE_API_KEY is not set. Add it to a .env file before running the app.")
    st.stop()


def normalize_model_name(model_name):
    if not model_name:
        return "models/gemini-2.5-flash"
    if model_name.startswith("models/"):
        return model_name
    return f"models/{model_name}"


def get_available_models(api_key):
    if "available_models" in st.session_state:
        return st.session_state["available_models"]

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        available = set()
        for model in client.models.list():
            supported_actions = getattr(model, "supported_actions", None)
            if supported_actions and "generateContent" in supported_actions:
                available.add(model.name)
        st.session_state["available_models"] = available
        return available
    except Exception:
        st.session_state["available_models"] = set()
        return set()


gemini_model = normalize_model_name(requested_model)
available_models = get_available_models(google_api_key)

# Sidebar for model selection
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    if available_models:
        model_list = sorted(list(available_models))
        selected_model = st.selectbox(
            "Choose your Gemini Model:",
            model_list,
            index=model_list.index(gemini_model) if gemini_model in model_list else 0
        )
        gemini_model = selected_model
    else:
        st.warning("⚠️ Could not fetch available models. Using default...")
        gemini_model = normalize_model_name(requested_model)
    
    st.markdown("---")
    st.info("💡 Free tier models available with no billing info required!")

chat = ChatGoogleGenerativeAI(
    model=gemini_model,
    temperature=0.5,
    google_api_key=google_api_key
)
if "flowmessages" not in st.session_state:
    st.session_state["flowmessages"] = [
        SystemMessage(content="""You are a witty, friendly British chatbot with a proper posh British personality! 🇬🇧

IMPORTANT: You MUST respond using authentic British slang and expressions. Here are examples to incorporate:
- Use "blimey", "brilliant", "ace", "wicked", "cheers", "ta", "mate", "gov'nor"
- Use phrases like "I fancy a cuppa", "Bob's your uncle", "sorted", "not half", "dead good"
- Occasionally use "innit", "bruv", "innit though", "safe blud" for London vibes
- Say things like "Right then", "Tell you what", "Fair do's", "Lovely jubbly"
- Use "reckon", "proper lush", "mint", "bonzer", "tidy", "belter"
- End messages with British expressions like "Cheerio!", "Toodles!", "Catch you later, mate!"

Your personality:
- You're enthusiastic and cheeky 
- You use humor and wit in your responses
- You're helpful but with a playful tone
- Always inject British charm into every response
- Mix standard responses with British slang naturally

Example response style:
"Blimey, that's a brilliant question, mate! Bob's your uncle, I reckon... [answer with British flair] Lovely jubbly!")

Now let's have a proper chinwag! What can I help you with today, gov'nor?""")
    ]


def get_gemini_response(query):
    st.session_state["flowmessages"].append(HumanMessage(content=query))
    answer = chat.invoke(st.session_state["flowmessages"])
    clean_text = extract_display_text(answer.content)
    st.session_state["flowmessages"].append(AIMessage(content=clean_text))
    return clean_text


def extract_display_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                # Hide model reasoning blocks and keep user-facing text only.
                if item.get("type") == "text" and item.get("text"):
                    text_parts.append(item["text"])
                elif "text" in item and item.get("text"):
                    text_parts.append(item["text"])
            elif isinstance(item, str):
                text_parts.append(item)

        if text_parts:
            return "\n\n".join(part.strip() for part in text_parts if part and part.strip())

    if isinstance(content, dict):
        if content.get("text"):
            return str(content["text"])

    return str(content)


# Display chat history with cool styling
st.markdown("<div style='margin-bottom: 150px;'>", unsafe_allow_html=True)

for message in st.session_state["flowmessages"]:
    if isinstance(message, HumanMessage):
        st.markdown(f"""
        <div class="user-message">
            👤 <b>You:</b><br>{message.content}
        </div>
        """, unsafe_allow_html=True)
    elif isinstance(message, AIMessage):
        ai_text = extract_display_text(message.content)
        st.markdown(f"""
        <div class="bot-message">
            🤖 <b>British Mate:</b><br>{ai_text}
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input section with fixed position
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Input:", 
            placeholder="Ask me something, bruv! 💬 (Press Enter to send)"
        )
    
    with col2:
        submit = st.form_submit_button("Send", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if submit:
    if not user_input.strip():
        st.warning("⚠️ Blimey, mate! You gotta type something first!")
    else:
        with st.spinner("🤔 Thinking... *adjusts monocle*"):
            response = get_gemini_response(user_input)
        st.rerun()