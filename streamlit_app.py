import os
from io import BytesIO

import openai
import pandas as pd
import streamlit as st
import streamlit_option_menu as st_om
from langchain.chat_models import ChatOpenAI

from chain_paper_sum import summarize_papers
from load_documents import delete_files


st.set_page_config(layout="wide")

# Get py file directory
dir_path = os.path.dirname(os.path.abspath(__file__))
uploaded_path = os.path.join(dir_path, "uploaded_files")


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()

    return processed_data


def format_output_text(output_text: str):
    output_text = output_text.split('\n')
    r = {key: output_text[i] for i, key in enumerate(["title", "author", "abstract", "data", "method", "conclusion"])}

    return r


def save_uploaded_file(uploaded_file):
    os.makedirs("uploaded_files", exist_ok=True)
    if isinstance(uploaded_file, list):
        for file in uploaded_file:
            save_file(file)
    else:
        save_file(uploaded_file)


def save_file(file):
    file_path = os.path.join("uploaded_files", file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())


with st.sidebar:
    selected = st_om.option_menu(
        "Main Menu",
        ["Chatbot", "PaperSum"]
    )

    with st.form("Settings"):
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        openai_api_base = st.text_input("OpenAI API Base URL")
        model_chat = st.selectbox("Chatbot model", ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"])
        model_sum = st.selectbox("Summarize model", ["gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4", "gpt-4-32k"])

        button_set = st.form_submit_button("Set")

    if button_set:
        os.environ['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_BASE'] = openai_api_base
        os.environ['MODEL_NAME_REFINED'] = model_chat
        os.environ['MODEL_NAME_STUFF'] = model_sum

        print(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_API_BASE"))
        st.success("OpenAI API Key and OpenAI API Base URL has been set.")

if selected == "Chatbot":
    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not os.getenv("OPENAI_API_KEY"):
            st.info("Please add your OpenAI API key in settings to continue.")
            st.stop()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)

if selected == "PaperSum":
    st.title("📝 Paper Summarization")
    with st.form("PaperSum"):
        paper_files = st.file_uploader("Upload your papers", accept_multiple_files=True, type=["pdf", "txt"])
        language = st.selectbox("Language", ["English", "Chinese", "Auto Detect"])
        language = "en" if language == "English" else language
        language = "cn" if language == "Chinese" else language
        auto_language = True if language == "Auto Detect" else False

        button_sum = st.form_submit_button("Summarize papers")

    if paper_files is not None and button_sum:
        for file in paper_files:
            save_uploaded_file(file)

        llm_sum = ChatOpenAI(model_name=os.getenv("MODEL_NAME_STUFF"))

        # Summarize papers
        df = summarize_papers(uploaded_path, llm=llm_sum, language=language, auto_language=auto_language)
        df_xlsx = to_excel(df)
        st.success("Summarized papers successfully")
        # Download results
        st.download_button(
            label='📥 Download PaperSum Results',
            data=df_xlsx,
            file_name='PaperSum_results.xlsx')
        delete_files(uploaded_path, ".txt")
        st.dataframe(df)
