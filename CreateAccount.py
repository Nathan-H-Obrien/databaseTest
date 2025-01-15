import streamlit as st
import sqlite3
import random
from datetime import datetime

def Create_account_page():
    st.title('Create an account')
    st.write('Enter your details')
    conn = st.connection('test.db', type='sql')
    with sqlite3.connect('test.db') as conn:
            id = random.randint(1, 999999)
            try:
                while conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone():
                    id = random.randint(1, 999999)
            except sqlite3.Error as e:
                pass
            username = st.text_input('Name: ')
            email = st.text_input('Email: ')
            password = st.text_input('Password: ', type='password')
            created_at = datetime.now()
            created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
            if st.button('Create account', key='create_account'):
                st.write('Account created successfully')
                with sqlite3.connect('test.db') as conn:
                    conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                    (id, username, email, password, created_at))
                    conn.commit()
            