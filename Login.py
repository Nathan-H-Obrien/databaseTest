import streamlit as st
import sqlite3
import random
from datetime import datetime

def Login_page():
    st.title('Login')
    email = st.text_input('Email:')
    password = st.text_input('Password:', type='password')
    st.button('Login', key='login', on_click=login(email, password))
def login(email, password):
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute('SELECT * FROM admin WHERE email = ? AND password = ?', (email, password))
                if cursor.fetchone():
                    st.write('Welcome admin')
                    while True:
                        st.button("Add User", key='add_user', on_click=add_user())
                        def add_user():    
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
                                st.button('Create account', key='add_user', on_click=create_user(id, username, email, password, created_at))
                        def create_user(id, username, email, password, created_at):
                                    with sqlite3.connect('test.db') as conn:
                                        conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                                        (id, username, email, password, created_at))
                                        conn.commit()
                        st.button("View Users", key='view_users', on_click=view_users())
                        def view_users():
                            try:
                                with sqlite3.connect('test.db') as conn:
                                    for row in conn.execute('SELECT * FROM users'):
                                        print(row)
                            except sqlite3.Error as e:
                                st.write('No users found')
                        
                        st.button("Exit", key='exit', on_click=exit())
                elif cursor.fetchone() is None:
                    cursor = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                    cursor.fetchone()
                    if cursor.fetchone():
                        st.write('Welcome user')
                        while True:
                            st.button('View profile', key='view_profile', on_click=view_profile())
                            def view_profile():
                                with sqlite3.connect('test.db') as conn:
                                    cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                                    for row in cursor:
                                        print(row)
                            st.button('Exit', key='exit', on_click=exit())
                else:
                    st.write('Invalid username or password')