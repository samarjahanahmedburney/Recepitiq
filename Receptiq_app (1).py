import streamlit as st
import matplotlib.pyplot as plt
import os
import tempfile

from core.ocr_engine import extract_text
from core.parser import parse_receipt
from core.analyzer import analyze_spending
from core.llm_advisor import generate_openai_advice, generate_gemini_advice


# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Recepitiq - AI Receipt Analyzer",
    page_icon="🧾",
    layout="wide"
)

st.title("🧾 Recepitiq")
st.subheader("AI-Powered Receipt Analyzer with LLM Insights")

st.markdown("---")


# -------------------------------------------------------
# File Upload
# -------------------------------------------------------
uploaded_file = st.file_uploader(
  "Upload a receipt image",
  type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

        st.success("Receipt uploaded successfully!")

# -------------------------------------------------------
# OCR
# -------------------------------------------------------
        with st.spinner("Extracting text using OCR..."):
           extracted_text = extract_text(temp_path)

        st.subheader("📄 Extracted Text")
        st.text(extracted_text)

# -------------------------------------------------------
# Parsing
# -------------------------------------------------------
        df = parse_receipt(extracted_text)

        if not df.empty:

# -------------------------------------------------------
# Analysis
# -------------------------------------------------------
          df, summary, total = analyze_spending(df)

          col1, col2 = st.columns(2)

          with col1:
              st.subheader("🛒 Detected Items")
              st.dataframe(df, use_container_width=True)

          with col2:
              st.subheader("📊 Spending Summary")
              st.dataframe(summary, use_container_width=True)

              st.metric("💰 Total Spending", f"${total:.2f}")

# -------------------------------------------------------
# Chart
# -------------------------------------------------------
          st.subheader("📈 Spending Distribution")

          fig, ax = plt.subplots()
          ax.pie(
              summary["price"],
          labels=summary["category"],
             autopct="%1.1f%%"
          )
          ax.set_title("Spending by Category")
          st.pyplot(fig)

          st.markdown("---")

# -------------------------------------------------------
# LLM Advice
# -------------------------------------------------------
          st.subheader("🤖 AI Financial Advice")

          llm_choice = st.selectbox(
              "Choose AI Model",
              ["OpenAI", "Gemini"]
          )

          if st.button("Generate Advice"):
              
               with st.spinner("Generating intelligent insights..."):
             
                   try:
                         if llm_choice == "OpenAI":
                              advice = generate_openai_advice(summary, total)
                         else:
                          advice = generate_gemini_advice(summary, total)
                                                                                        

                         st.success("Advice Generated Successfully!")
                         st.write(advice)

                   except Exception as e:
                         st.error("Error generating AI advice.")
                         st.write(str(e))

        else:
          st.warning("No valid items detected from this receipt.")

# Cleanup temp file
        os.remove(temp_path)

else:
  st.info("Upload a receipt image to begin analysis.")