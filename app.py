import streamlit as st
import joblib
from pathlib import Path

MODEL_PATH = Path("models/baseline_tfidf_logreg.joblib")

st.set_page_config(
    page_title="Climate Stance Detector",
    page_icon="🌍",
    layout="centered"
)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )
    return joblib.load(MODEL_PATH)

st.title("🌍 Climate Stance Detector")

st.markdown(
    """
    Enter a sentence to identify its stance towards the claim:

    **"Climate change and global warming is a serious concern."**

    Supported text: Hindi, Bengali, Hinglish, Romanized Hindi and English.
    """
)

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

language = st.selectbox(
    "Select sentence language",
    [
        "Hindi",
        "Hindi_Romanized",
        "Bengali",
        "Bengali_Romanized",
        "Hinglish",
        "English"
    ]
)

text = st.text_area(
    "Enter your sentence",
    placeholder="Example: Climate change is a serious global problem...",
    height=150
)

if st.button("Predict Stance", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter a sentence.")
    else:
        try:
            # Current model was trained with a language prefix.
            # Ask the user to select the language for this prediction.
            model_text = f"[LANG_{language}] {text.strip()}"
            prediction = model.predict([model_text])[0]

            st.divider()
            st.subheader("Prediction")

            colors = {
                "Favour": "green",
                "Against": "red",
                "None": "blue"
            }

            st.markdown(
                f"### :{colors.get(prediction, 'gray')}[{prediction}]"
            )

            st.caption(
                "This is an experimental prediction from the current baseline model. "
                "It may be unreliable, especially for underrepresented classes."
            )

        except Exception as e:
            st.error(f"Prediction failed: {e}")
