import streamlit as st
import google.generativeai as genai

st.title("📚 NEX CRA AI")
st.write("AI Homework Assistant - Like ChatGPT!")

genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

q = st.text_input("Ask your homework question:")
if st.button("Ask"):
    if q:
        with st.spinner("Thinking..."):
            ans = model.generate_content(q)
            st.success(ans.text)
    else:
        st.warning("Please type a question first!")
