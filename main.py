import streamlit as st

st.set_page_config(page_title="NEX CRA AI", page_icon="📚")
st.title("📚 NEX CRA AI")
st.write("AI Homework Assistant")

question = st.text_input("Ask your homework question:")

if st.button("Ask"):
    if question:
        st.success("You asked: " + question)
        st.write("This is a demo answer. Connect your OpenAI key to get real answers!")
    else:
        st.warning("Please type a question first!")
