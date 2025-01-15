import streamlit as st
import sqlite3
import random
from datetime import datetime

def Login_page():
    st.title('Login')
    email = st.text_input('Email:')
    password = st.text_input('Password:', type='password')
    if st.button('Login', key='login'):
        conn = st.connection('test.db', type='sql')
        with conn.session as conn:
            cursor = conn.execute('SELECT * FROM admin WHERE email = ? AND password = ?', (email, password))
            cursor2 = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            if cursor.fetchone():
                st.write('Welcome admin')
                option = st.selectbox('Select an option', ['Add User', 'View Users', 'Logout'])
                if option == 'Add User':
                    st.write('Add a user')
                    with conn.session as conn:
                        id = random.randint(1, 999999)
                        while conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone():
                            id = random.randint(1, 999999)
                        username = st.text_input('Name: ')
                        email = st.text_input('Email: ')
                        password = st.text_input('Password: ', type='password')
                        created_at = datetime.now()
                        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                        if st.button('Create account', key='create_account'):
                            with conn.session as conn:
                                conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                                (id, username, email, password, created_at))
                                conn.commit()
                    if option == 'View Users':
                        with conn.session as conn:
                            for row in conn.execute('SELECT * FROM users'):
                                st.write(row)
                    if option == 'Logout':
                        exit()
            elif cursor2.fetchone():
                st.write('Welcome user')
                if st.button('View profile', key='view_user_profile'):
                    with conn.session as conn:
                        cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                        for row in cursor:
                            st.write(row)
                if st.button('Logout', key='logout_user'):
                    exit()
            else:
                st.write('Invalid username or password')