

# import streamlit as st
# import pandas as pd
# from energy_advisor import build_graph, EnergyState
# import openai

# st.set_page_config(page_title="Houston Energy Advisor", layout="wide")
# st.title("⚡ Houston Energy Advisor")

# with st.sidebar:
#     st.header("Upload & Settings")
#     uploaded_file = st.file_uploader("Upload your energy CSV", type=["csv"])
#     zone = st.text_input("Zone (optional)", value="")
#     dry_llm = st.checkbox("Use rule-based tips only (no GPT)", value=False)

# if uploaded_file:
#     csv_path = "uploaded_energy.csv"
#     with open(csv_path, "wb") as f:
#         f.write(uploaded_file.read())

#     df = pd.read_csv(csv_path)
#     st.subheader("Preview of Uploaded Data")
#     st.dataframe(df.head(), use_container_width=True)

#     time_col = st.selectbox("Select time column", options=df.columns, key="time_col")
#     value_col_options = [col for col in df.columns if col != time_col]
#     value_col = st.selectbox("Select value column", options=value_col_options, key="value_col")

#     run_analysis = st.button("Analyze", type="primary")
#     if run_analysis:
#         with st.spinner("Analyzing your data..."):
#             state = {
#                 "csv_path": csv_path,
#                 "time_col": time_col,
#                 "value_col": value_col,
#                 "zone": zone if zone else None,
#                 "dry_llm": dry_llm,
#             }
#             app = build_graph()
#             try:
#                 result = app.invoke(state)
#                 col1, col2 = st.columns([1, 1])
#                 with col1:
#                     with st.expander("📊 KPIs", expanded=True):
#                         st.json(result["kpis"])
#                 with col2:
#                     with st.expander("📈 Energy Usage Plot", expanded=True):
#                         st.image(result["plot_path"], use_column_width=True)
#                 with st.expander("💡 Tips & Recommendations", expanded=True):
#                     st.markdown(result["tips"])
#             except Exception as e:
#                 st.error(f"Error: {e}")
# else:
#     st.info("Please upload a CSV file from the sidebar to begin.")



# import openai

# import openai

# st.markdown("---")
# st.header("💬 Energy Chatbot")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Try to get context from the last analysis if available
# context = ""
# if uploaded_file and "result" in locals():
#     kpis = result.get("kpis", {})
#     context = (
#         "Here are the user's energy KPIs from their uploaded data:\n"
#         + "\n".join([f"{k}: {v}" for k, v in kpis.items()])
#         + "\nYou may use this data to answer questions if relevant."
#     )
# else:
#     context = (
#         "You are an expert energy advisor. Answer questions about energy, electricity, efficiency, and related topics in a helpful and concise way."
#     )

# user_question = st.text_input("Ask any energy-related question:")

# if st.button("Ask"):
#     if not user_question.strip():
#         st.warning("Please enter a question.")
#     else:
#         with st.spinner("Thinking..."):
#             try:
#                 client = openai.OpenAI()
#                 response = client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": context},
#                         {"role": "user", "content": user_question}
#                     ],
#                     max_tokens=300,
#                 )
#                 answer = response.choices[0].message.content
#                 st.session_state.chat_history.append(("You", user_question))
#                 st.session_state.chat_history.append(("Bot", answer))
#             except Exception as e:
#                 st.error(f"Error: {e}")

# if st.session_state.chat_history:
#     for speaker, msg in reversed(st.session_state.chat_history):
#         st.markdown(f"**{speaker}:** {msg}")

import streamlit as st
import pandas as pd
from energy_advisor import build_graph, EnergyState
import openai

# Set a custom theme using Streamlit config (add this to .streamlit/config.toml for full effect)
st.set_page_config(page_title="Energy Advisor", layout="wide", page_icon="⚡")

# Sidebar for upload/settings and chatbot toggle
with st.sidebar:
    st.header("Upload & Settings")
    uploaded_file = st.file_uploader("Upload your energy CSV", type=["csv"])
    zone = st.text_input("Zone (optional)", value="")
    dry_llm = st.checkbox("Use rule-based tips only (no GPT)", value=False)
    st.markdown("---")
    show_chatbot = st.checkbox("💬 Open Chatbot", value=False)

# Main content area
st.markdown(
    """
    <style>
    body {
        background-color: #181c25 !important;
    }
    .stApp {
        background-color: #181c25;
    }
    .card {
        background: #23272f;
        border-radius: 12px;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.08);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00BFFF;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-subtitle {
        font-size: 1.1rem;
        color: #b0b8c1;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='color:#00BFFF; font-size:2.5rem;'>⚡ Energy Advisor</h1>",
    unsafe_allow_html=True,
)

# ...existing sidebar and style code...

if uploaded_file:
    csv_path = "uploaded_energy.csv"
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_csv(csv_path)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head(), use_container_width=True)

    time_col = st.selectbox("Select time column", options=df.columns, key="time_col")
    value_col_options = [col for col in df.columns if col != time_col]
    value_col = st.selectbox("Select value column", options=value_col_options, key="value_col")

    run_analysis = st.button("Analyze", type="primary")
    # Store result in session state so chatbot can access it
    if "result" not in st.session_state:
        st.session_state.result = None

    if run_analysis:
        with st.spinner("Analyzing your data..."):
            state = {
                "csv_path": csv_path,
                "time_col": time_col,
                "value_col": value_col,
                "zone": zone if zone else None,
                "dry_llm": dry_llm,
            }
            app = build_graph()
            try:
                result = app.invoke(state)
                st.session_state.result = result  # Save for chatbot context
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.result = None

    # Show results if available
    result = st.session_state.get("result")
    if result:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 KPIs</div>', unsafe_allow_html=True)
            st.json(result["kpis"])
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📈 Energy Usage Plot</div>', unsafe_allow_html=True)
            st.image(result["plot_path"], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 Tips & Recommendations</div>', unsafe_allow_html=True)
        st.markdown(result["tips"])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Chatbot Section (always below analysis/results) ---
    if show_chatbot:
        st.markdown("---")
        st.header("💬 Energy Chatbot")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Hide "Press Enter to apply" hint for text_area
        st.markdown("""
            <style>
            .stTextArea > div > div > textarea + div {display: none;}
            </style>
        """, unsafe_allow_html=True)

        # Use context from latest result if available
        context = ""
        if result:
            kpis = result.get("kpis", {})
            context = (
                "Here are the user's energy KPIs from their uploaded data:\n"
                + "\n".join([f"{k}: {v}" for k, v in kpis.items()])
                + "\nYou may use this data to answer questions if relevant."
            )
        else:
            context = (
                "You are an expert energy advisor. Answer questions about energy, electricity, efficiency, and related topics in a helpful and concise way."
            )

        user_question = st.text_area(
            "Ask any energy-related question (Shift+Enter for newline):",
            key="chat_input",
            height=80,
            placeholder="Type your question here..."
        )

        uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

        if st.button("Ask", key="ask_btn"):
            if not user_question.strip() and not uploaded_image:
                st.warning("Please enter a question or upload an image.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        client = openai.OpenAI()
                        messages = [
                            {"role": "system", "content": context},
                            {"role": "user", "content": user_question}
                        ]
                        # If image is uploaded, add it to the message (for GPT-4o or GPT-4-vision-preview)
                        if uploaded_image:
                            import base64
                            image_bytes = uploaded_image.read()
                            b64_image = base64.b64encode(image_bytes).decode()
                            messages.append({
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": user_question},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{b64_image}"
                                        }
                                    }
                                ]
                            })
                            st.image(image_bytes, caption="Uploaded Image", use_container_width=True)
                            # Use GPT-4o or GPT-4-vision-preview for image support
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages,
                                max_tokens=300,
                            )
                        else:
                            response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=messages,
                                max_tokens=300,
                            )
                        answer = response.choices[0].message.content
                        st.session_state.chat_history.append(("You", user_question))
                        if uploaded_image:
                            st.session_state.chat_history.append(("You (image)", "[Image uploaded]"))
                        st.session_state.chat_history.append(("Bot", answer))
                    except Exception as e:
                        st.error(f"Error: {e}")

        # ...inside the chatbot section, replace this block:
    # if st.session_state.chat_history:
    #     for speaker, msg in reversed(st.session_state.chat_history):
    #         st.markdown(f"**{speaker}:** {msg}")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.chat_history:
        for speaker, msg in reversed(st.session_state.chat_history):
            if speaker.startswith("You"):
                st.markdown(
                    f"""
                    <div style='background-color:#1e293b; color:#f1f8ff; padding:0.7em 1em; border-radius:10px; margin-bottom:0.5em; text-align:right;'>
                        <b style='color:#38bdf8;'>{speaker}:</b> {msg}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif speaker == "Bot":
                st.markdown(
                    f"""
                    <div style='background-color:#25324d; color:#e6f2ff; padding:0.7em 1em; border-radius:16px; margin-bottom:0.5em; text-align:left;'>
                        <b style='color:#38bdf8;'>Bot:</b> {msg}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"**{speaker}:** {msg}")
else:
    st.info("Please upload a CSV file from the sidebar to begin.")

