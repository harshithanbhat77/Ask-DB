import streamlit as st
from pathlib import Path
from custom_sql_toolkit import CustomSQLToolkit
from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from session_manager import load_session, save_session
from custom_sql_prompt import sql_prompt_template
import json


st.set_page_config(page_title="LangChain SQL Chat", layout="wide")
st.title("Chat with your Database")

user_id = st.text_input("Enter your User ID:", placeholder="e.g., harshitha123", key="user_id_main")
if not user_id:
    st.warning("Please enter your User ID to continue.")
    st.stop()

if "session_data" not in st.session_state:
    st.session_state.session_data = load_session()

session_data = st.session_state.session_data


if "chat_history" not in st.session_state:
    old_history = session_data.get("chat_history", {})
    if isinstance(old_history, list): 
        old_history = {"default_user": old_history}
    st.session_state.chat_history = old_history

user_history = st.session_state.chat_history.get(user_id, [])

with st.sidebar:
    st.header("Database Connection")

    db_type = st.selectbox("Select DB Type", ["SQLite", "MySQL", "PostgreSQL"])
    if db_type == "SQLite":
        db_path = st.text_input("SQLite file path", "sample.db")
        db_uri = f"sqlite:///{db_path}"
    elif db_type == "MySQL":
        host = st.text_input("Host", "localhost")
        user = st.text_input("User", "root")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database name")
        db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    else:
        host = st.text_input("Host", "localhost")
        user = st.text_input("User", "postgres")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database name")
        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"

    if st.button("Connect"):
        try:
            db = SQLDatabase.from_uri(db_uri)
            llm = OllamaLLM(model="llama3.1")
            toolkit = CustomSQLToolkit(db=db, llm=llm)
            agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
            st.session_state.agent = agent
            st.session_state.db_connected = True
            st.success("Connected successfully!")

            session_data["db_uri"] = db_uri
            save_session(session_data)

        except Exception as e:
            st.error(f"Connection failed: {e}")

if "agent" not in st.session_state:
    st.info(" Connect to your database from the sidebar to start chatting.")
    st.stop()

st.divider()
st.subheader("Chat Window")

for msg in user_history:
    if "query" in msg:
        with st.chat_message("user"):
            st.markdown(msg["query"])
    if "response" in msg:
        with st.chat_message("assistant"):
            st.markdown(msg["response"])

if prompt := st.chat_input("Ask your database anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(prompt)
            except Exception as e:
                response = f"Error: {e}"
            st.markdown(response)

  
    user_history.append({"query": prompt, "response": response})
    st.session_state.chat_history[user_id] = user_history
    session_data["chat_history"] = st.session_state.chat_history
    save_session(session_data)


st.sidebar.markdown("---")
if st.sidebar.button(" Clear My Chat History"):
    st.session_state.chat_history[user_id] = []
    session_data["chat_history"] = st.session_state.chat_history
    save_session(session_data)
    st.success("Chat history cleared for this user!")
