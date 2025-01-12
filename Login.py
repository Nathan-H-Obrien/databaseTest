import streamlit as st
import sqlite3
import random
from datetime import datetime

def Login_page():
    st.title('Login')
    email = st.text_input('Email:')
    password = st.text_input('Password:', type='password')
    if st.button('Login', key='0'):
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute('SELECT * FROM admin WHERE email = ? AND password = ?', (email, password))
                cursor2 = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                if cursor.fetchone():
                    st.write('Welcome admin')
                    while True:
                        if st.button("Add User", key='5'):
                            st.write('Add a user')
                            with sqlite3.connect('test.db') as conn:
                                id = random.randint(1, 999999)
                                try:
                                    while conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone():
                                        id = random.randint(1, 999999)
                                except sqlite3.Error:
                                    pass
                                username = st.text_input('Name: ')
                                email = st.text_input('Email: ')
                                password = st.text_input('Password: ', type='password')
                                created_at = datetime.now()
                                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                            if st.button('Create account', key='4'):
                                    with sqlite3.connect('test.db') as conn:
                                        conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                                        (id, username, email, password, created_at))
                                        conn.commit()
                        if st.button("View Users", key='3'):
                                with sqlite3.connect('test.db') as conn:
                                    for row in conn.execute('SELECT * FROM users'):
                                        st.write(row)
                        
                        if st.button("logout", key='2'):
                            break
                elif cursor2.fetchone():
                        st.write('Welcome user')
                        while True:
                            if st.button('View profile', key='1'):
                                with sqlite3.connect('test.db') as conn:
                                    cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                                    for row in cursor:
                                        print(row)
                            if st.button('logout', key='2'):
                                break
                else:
                    st.write('Invalid username or password')