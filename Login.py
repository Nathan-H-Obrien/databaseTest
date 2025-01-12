import streamlit as st
import sqlite3
import random
from datetime import datetime

def Login_page():
    st.title('Login')
    email = st.text_input('Email:')
    password = st.text_input('Password:', type='password')
    if st.button('Login', key='login'):
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute('SELECT * FROM admin WHERE email = ? AND password = ?', (email, password))
                cursor2 = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                if cursor.fetchone():
                    st.write('Welcome admin')
                    while True:
                        if st.button("Add User", key='make_user'):
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
                            if st.button('Create account', key='make_account'):
                                    with sqlite3.connect('test.db') as conn:
                                        conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                                        (id, username, email, password, created_at))
                                        conn.commit()
                        if st.button("View Users", key='view_users'):
                                with sqlite3.connect('test.db') as conn:
                                    for row in conn.execute('SELECT * FROM users'):
                                        st.write(row)
                        
                        if st.button("logout", key='exit'):
                            break
                elif cursor2.fetchone():
                    cursor = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                    cursor.fetchone()
                    if cursor.fetchone():
                        st.write('Welcome user')
                        while True:
                            if st.button('View profile', key='view_profile'):
                                with sqlite3.connect('test.db') as conn:
                                    cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                                    for row in cursor:
                                        print(row)
                            if st.button('logout', key='logout'):
                                break
                else:
                    st.write('Invalid username or password')