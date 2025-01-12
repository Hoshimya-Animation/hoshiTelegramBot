import sqlite3
from datetime import datetime,timedelta

def start_db():
    #Connection to SQL DB
    connect = sqlite3.connect('telegramDataBot.db')
    cursor = connect.cursor()
    #Create table if not exist
    db_table_query = '''
    CREATE TABLE IF NOT EXISTS databot(
        user_id INT PRIMARY KEY,
        language VARCHAR(10),
        age INT,
        registration_date DATE
    );
    '''
    cursor.execute(db_table_query)
    connect.commit()
    cursor.close()
    connect.close()


def updateIDUser(user_id, language=None, age=None):
    connection = sqlite3.connect('telegramDataBot.db')
    cursor = connection.cursor()
    
    # Check if the user_id already exists
    cursor.execute('SELECT user_id, language, age, registration_date FROM databot WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        # Insert new user_id with NULL values for language, age and registration_date if it doesn't exist
        cursor.execute('''
            INSERT INTO databot (user_id, language, age, registration_date)
            VALUES (?, NULL, NULL, NULL);
        ''', (user_id,))
    else:
        existing_language = result[1]
        existing_age = result[2]
        existing_registration_date = result[3]
        
        # Update language only if it is provided and the existing value is NULL
        if language is not None and existing_language is None:
            cursor.execute('''
                UPDATE databot
                SET language = ?
                WHERE user_id = ?;
            ''', (language, user_id))
        
        # Update age and registration_date only if age is provided and the existing value is NULL
        if age is not None and existing_age is None:
            registration_date = datetime.now().date()
            cursor.execute('''
                UPDATE databot
                SET age = ?, registration_date = ?
                WHERE user_id = ?;
            ''', (age, registration_date, user_id))
    
    connection.commit()
    connection.close()


def set_language(user_id, language): 
    connection = sqlite3.connect('telegramDataBot.db') 
    cursor = connection.cursor() 
    cursor.execute("UPDATE databot SET language = ? WHERE user_id = ?", (language, user_id)) 
    connection.commit() 
    cursor.close() 
    connection.close()


def get_language(user_id): 
    connection = sqlite3.connect('telegramDataBot.db') 
    cursor = connection.cursor() 
    cursor.execute("SELECT language FROM databot WHERE user_id = ?", (user_id,)) 
    result = cursor.fetchone() 
    cursor.close() 
    connection.close() 
    return result[0] if result else None

def updateAge(user_id, age):
    age = int(age)
    registration_date = datetime.now().date()
    connection = sqlite3.connect('telegramDataBot.db') 
    cursor = connection.cursor() 
    cursor.execute(''' 
        UPDATE databot 
        SET age = ?, registration_date = ?
        WHERE user_id = ?
    ''', (age, registration_date, user_id))
    connection.commit() 
    cursor.close() 
    connection.close()

def get_user_age(user_id):
    connection = sqlite3.connect('telegramDataBot.db')
    cursor = connection.cursor()

    # Query to get the age of the user
    cursor.execute('SELECT age FROM databot WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    # Close the connection
    connection.close()

    # If the result is not None, return the age, otherwise return None
    if result is not None and result[0] is not None:
        return result[0]
    else:
        return None


def update_age_automatically(): 
    today = datetime.now().date()
    connection = sqlite3.connect('telegramDataBot.db')  
    cursor = connection.cursor() 
    cursor.execute('SELECT user_id, age, registration_date FROM databot') 
    users = cursor.fetchall() 
    for user in users: 
        user_id, age, registration_date = user
        if registration_date is not None:
            registration_date = datetime.strptime(registration_date, '%Y-%m-%d').date() # Check if a year has passed since registration 
            if today >= registration_date + timedelta(days=365): 
                new_age = age + 1
                new_registration_date = today 
                cursor.execute(''' UPDATE databot SET age = ?, registration_date = ? WHERE user_id = ? ''', (new_age, new_registration_date, user_id)) 
                connection.commit()
