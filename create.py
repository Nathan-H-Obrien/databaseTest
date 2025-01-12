import sqlite3
from datetime import datetime
import random
import streamlit as st


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

conn = st.connection('test2.db', type='sqlite3')
cursor = conn.cursor()


st.button('Create an account')
st.button('Login')

if st.button('Create an account'):
    st.write('Create an account')
    st.write('Enter your details')
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
        st.button('Create account')
        if st.button('Create account'):
            with sqlite3.connect('test.db') as conn:
                conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                (id, username, email, password, created_at))
                conn.commit()


if st.button('Login'):
    st.write('Login')
    email = st.text_input('Email:')
    password = st.text_input('Password:', type='password')
    st.button('Login')
    if st.button('Login'):
        with sqlite3.connect('test.db') as conn:
            cursor = conn.execute('SELECT * FROM admin WHERE email = ? AND password = ?', (email, password))
            if cursor.fetchone():
                print('Welcome admin')
                while True:
                    print('1. Add user')
                    print('2. List users')
                    print('3. Exit')
                    choice = input('Enter your choice: ')
                    if choice == '1':
                        st.write('Create an account')
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
                            st.button('Create account')
                            if st.button('Create account'):
                                with sqlite3.connect('test.db') as conn:
                                    conn.execute('INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)', 
                                    (id, username, email, password, created_at))
                                    conn.commit()
                    elif choice == '2':
                        try:
                            with sqlite3.connect('test.db') as conn:
                                for row in conn.execute('SELECT * FROM users'):
                                    print(row)
                        except sqlite3.Error as e:
                            print("No users found")
                    elif choice == '3':
                        exit()
            elif cursor.fetchone() is None:
                cursor = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                user = True if cursor.fetchone() else False
                if cursor.fetchone():
                    print('Welcome user')
                    while True:
                        print('1. View profile')
                        print('2. Exit')
                        choice = input('Enter your choice: ')
                        if choice == '1':
                            with sqlite3.connect('test.db') as conn:
                                cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                                for row in cursor:
                                    print(row)
                        elif choice == '2':
                            exit()
            else:
                print('Invalid username or password')
                exit()

conn.close()