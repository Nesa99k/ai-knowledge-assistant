import httpx
import streamlit as st
from pathlib import Path
import os


from questions import QUESTIONS

BASE_DIR = Path(__file__).resolve().parent

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/ask",
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon=str(BASE_DIR / "page_icon.png"),
    layout="wide",
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(111, 58, 160, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 80%,
                rgba(74, 40, 120, 0.25),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #08070d 0%,
                #100b18 50%,
                #08070d 100%
            );
        color: #f5f3f8;
    }
    /* Remove Streamlit top bar */
    header[data-testid="stHeader"] {
    display: none;
    }
    [data-testid="stAppViewContainer"] {
      background: transparent;
    }
    [data-testid="stHeader"] {
    background: transparent;
    }
    
    /* Main content */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #aaa3b5;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.055);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 20px;
        padding: 1.4rem;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.25);
    }

    /* Robot placeholder */
    .robot-placeholder {
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        border: 1px dashed rgba(180, 130, 255, 0.35);
        background: rgba(120, 70, 180, 0.08);
        color: #9d8aaa;
        text-align: center;
        font-size: 0.95rem;
    }

    .robot-icon {
        font-size: 4rem;
        margin-bottom: 0.7rem;
    }

    /* Conversation */
    .message {
        display: flex;
        gap: 12px;
        margin: 1rem 0;
        align-items: flex-start;
    }

    .avatar {
        min-width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        font-size: 1.25rem;
    }

    .message-content {
        flex: 1;
        background: rgba(255, 255, 255, 0.055);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    .message-label {
        font-size: 0.8rem;
        color: #9f8faf;
        margin-bottom: 0.35rem;
    }

    /* Reference */
    .reference {
        margin-top: 1rem;
        padding: 0.8rem 1rem;
        border-left: 3px solid #8d5bc7;
        background: rgba(141, 91, 199, 0.08);
        border-radius: 8px;
        color: #aaa3b5;
        font-size: 0.85rem;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(180, 130, 255, 0.35);
        background: linear-gradient(
            135deg,
            #6d3fa0,
            #4c286f
        );
        color: white;
        font-weight: 600;
        padding: 0.65rem;
    }

    .stButton > button:hover {
        border-color: rgba(220, 190, 255, 0.65);
        background: linear-gradient(
            135deg,
            #7b49b2,
            #59317e
        );
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="app-title">🤖 AI Knowledge Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Clinical nutrition knowledge assistant'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Top section
# --------------------------------------------------

left_column, right_column = st.columns(
    [1, 1.5],
    gap="large",
)


with left_column:

    # st.markdown(
    #     """
    #     <div class="glass-card">
    #     """,
    #     unsafe_allow_html=True,
    # )

    st.image(
        "ui/robot.png",
        width=500,
    )

    # st.markdown(
    #     "</div>",
    #     unsafe_allow_html=True,
    # )


with right_column:

    section = st.selectbox(
        "Select a disability",
        list(QUESTIONS.keys()),
    )

    question = st.selectbox(
        "Select a question",
        QUESTIONS[section],
    )

    ask = st.button("Ask")

# --------------------------------------------------
# Ask API
# --------------------------------------------------

if ask:

    try:

        response = httpx.post(
            API_URL,
            json={
                "question": question,
                "section": section,
            },
            timeout=120.0,
        )

        if response.status_code == 200:

            data = response.json()

            st.markdown(
                "### Conversation"
            )

            # User message
            st.markdown(
                f"""
                <div class="message">
                    <div class="avatar">👤</div>
                    <div class="message-content">
                        <div class="message-label">
                            You
                        </div>
                        {question}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Assistant message
            st.markdown(
                f"""
                <div class="message">
                    <div class="avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-label">
                            AI Knowledge Assistant
                        </div>
                        {data["answer"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Reference
            st.markdown(
                f"""
                <div class="reference">
                    📚 Source: {section}
                    <br>
                    Knowledge base reference
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.error(
                f"API error: {response.status_code}"
            )

    except httpx.RequestError:

        st.error(
            "Could not connect to the API. "
            "Make sure FastAPI is running."
        )
