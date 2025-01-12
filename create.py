import sqlite3
from datetime import datetime
import random
import streamlit as st
from Login import Login_page
from CreateAccount import Create_account_page


try:
    with sqlite3.connect('test2.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            password TEXT,
            created_at TIMESTAMP
            )
        ''')

    with sqlite3.connect('test2.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY,
            email TEXT,
            password TEXT
            )
        ''')

except sqlite3.Error as e:
    pass


pages = {
    'Login': Login_page,
    'Create account': Create_account_page
}

st.sidebar.title('Navigation')
if 'page' not in st.session_state:
    st.session_state.page = list(pages.keys())[0]

for page_name in pages:
    if st.sidebar.button(page_name):
        st.session_state.page = page_name

if st.session_state.page in pages:
    pages[st.session_state.page]()
else:
    st.error("Selected page not found.")
