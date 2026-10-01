import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000/ask"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cricket RAG Assistant",
    page_icon="🏏",
    layout="centered"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🏏 Cricket RAG Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions from the cricket knowledge base'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Cricket RAG")

    st.write(
        """
        This application uses:

        • Streamlit  
        • FastAPI  
        • ChromaDB  
        • Hugging Face Embeddings  
        • Ollama  
        • Llama 3.2:1b  
        • Docker
        """
    )

    st.divider()

    st.subheader("Example Questions")

    st.write("Who won the 2011 Cricket World Cup?")
    st.write("Who scored 765 runs in the 2023 World Cup?")
    st.write("Who was India's captain in the 1983 World Cup?")
    st.write("Where was the 2011 World Cup final played?")

    st.divider()

    # Clear conversation
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ============================================================
# USER INPUT
# ============================================================

question = st.chat_input(
    "Ask a cricket question..."
)


# ============================================================
# HANDLE QUESTION
# ============================================================

if question:

    # Show user question
    with st.chat_message("user"):

        st.write(question)

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # --------------------------------------------------------
    # CALL FASTAPI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Searching cricket knowledge base..."
            ):

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120
                )

            # Make sure HTTP request succeeded
            response.raise_for_status()

            # Convert response to JSON
            data = response.json()

            # ------------------------------------------------
            # GET ANSWER DIRECTLY FROM FASTAPI
            # ------------------------------------------------

            answer = data.get(
                "answer",
                "No answer returned."
            )

            sources = data.get(
                "sources",
                []
            )

            method = data.get(
                "method",
                "unknown"
            )

            # ------------------------------------------------
            # DISPLAY ANSWER
            # ------------------------------------------------

            st.markdown("### Answer")

            st.write(answer)

            st.caption(
                f"Answer method: {method}"
            )

            # ------------------------------------------------
            # DISPLAY SOURCES
            # ------------------------------------------------

            if sources:

                st.markdown("### Sources")

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    source_name = source.get(
                        "source",
                        "Unknown"
                    )

                    distance = source.get(
                        "distance_score",
                        "N/A"
                    )

                    content = source.get(
                        "content",
                        ""
                    )

                    with st.expander(
                        f"Source {i}: {source_name}"
                    ):

                        st.write(
                            f"Distance score: {distance}"
                        )

                        st.write(content)

            # ------------------------------------------------
            # DEBUG: SHOW EXACT BACKEND RESPONSE
            # ------------------------------------------------

            with st.expander(
                "Debug: FastAPI response"
            ):

                st.json(data)

            # Store EXACT answer returned by backend
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Make sure Docker is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "FastAPI took too long to respond."
            )

        except requests.exceptions.HTTPError as error:

            st.error(
                f"FastAPI returned an HTTP error: {error}"
            )

        except ValueError:

            st.error(
                "FastAPI returned an invalid JSON response."
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )