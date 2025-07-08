import openai
from sl import speak, listen
import streamlit as st
import dotenv
import os
import time

#------------------------------------------------------------------------- Load API key -------------------------------------------------------------------------
dotenv.load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
wakeup_word = "hello"

#------------------------------------------------------------------------- Initialize OpenRouter client -------------------------------------------------------------------------
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

#------------------------------------------------------------------------- Streamlit setup -------------------------------------------------------------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🎙️ Voice AI Assistant")

#------------------------------------------------------------------------- Session states -------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "active" not in st.session_state:
    st.session_state.active = False

#------------------------------------------------------------------------- Start/Stop buttons -------------------------------------------------------------------------
if not st.session_state.active:
    if st.button("▶️ Start Assistant"):
        st.session_state.active = True
        st.rerun()
else:
    if st.button("🛑 Stop Assistant"):
        st.session_state.active = False
        st.success("🛑 Assistant stopped.")
        st.rerun()

#------------------------------------------------------------------------- Listening logic -------------------------------------------------------------------------
if st.session_state.active:
    st.success("✅ Assistant is active! Say 'hello' to begin.")
    speech = listen()

    if wakeup_word in speech.lower():
        st.success("✅ Wake word detected. Listening for your question...")
        user_input = listen()

        if not user_input:
            st.warning("⚠️ No input detected.")
        else:
            user_input = user_input.strip() + " in one sentence"
            st.info("🧍 YOU: " + user_input)

            try:
                resp = client.chat.completions.create(
                    model="deepseek/deepseek-r1:free",
                    messages=[{"role": "user", "content": user_input}]
                )
                output = resp.choices[0].message.content
                st.success("🤖 AI: " + output)
                speak(output)
                st.session_state.history.append({"user": user_input, "ai": output})
                time.sleep(1.5)
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {e}")
                speak("Sorry, I encountered an error.")
    else:
        st.warning("❌ Wake word not detected. Listening again...")
        time.sleep(1.5)
        st.rerun()

#------------------------------------------------------------------------- Show history only when assistant is OFF -------------------------------------------------------------------------
if not st.session_state.active and st.session_state.history:
    st.markdown("### 🗂️ Conversation History")
    for entry in st.session_state.history[::-1]:
        st.markdown(f"**🧍 YOU:** {entry['user']}")
        st.markdown(f"**🤖 AI:** {entry['ai']}")
