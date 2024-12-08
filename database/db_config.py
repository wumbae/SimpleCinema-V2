import sqlite3
import os
import uuid
import hashlib
from datetime import datetime, timedelta

DB_FILE = "cinema_booking.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def generate_id():
    return str(uuid.uuid4())

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')

        # Cinemas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id TEXT PRIMARY KEY,
            city TEXT NOT NULL,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
        ''')

        # Screens
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS screens (
            id TEXT PRIMARY KEY,
            screenNumber TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            type TEXT NOT NULL,
            cinema_id TEXT NOT NULL,
            FOREIGN KEY (cinema_id) REFERENCES cinemas (id)
        )
        ''')

        # Films
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating TEXT NOT NULL,
            duration INTEGER NOT NULL,
            description TEXT,
            actors TEXT
        )
        ''')

        # Sessions
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            sessionID TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            filmId TEXT NOT NULL,
            screenId TEXT NOT NULL,
            city TEXT NOT NULL,
            FOREIGN KEY (filmId) REFERENCES films (id),
            FOREIGN KEY (screenId) REFERENCES screens (id)
        )
        ''')

        # Bookings
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            bookingID TEXT UNIQUE NOT NULL,
            bookingDate TEXT NOT NULL,
            date TEXT NOT NULL,
            seats INTEGER NOT NULL,
            ticketType TEXT NOT NULL,
            userId TEXT NOT NULL,
            sessionId TEXT NOT NULL,
            totalPrice FLOAT NOT NULL,
            FOREIGN KEY (userId) REFERENCES users (id),
            FOREIGN KEY (sessionId) REFERENCES sessions (id)
        )
        ''')

        conn.commit()
        conn.close()

def initialize_database():
    create_database()
    from database.db_manager import DatabaseManager
    db = DatabaseManager()

    # Clear tables for demonstration
    for t in ['users','cinemas','screens','films','sessions','bookings']:
        db.execute_query(f"DELETE FROM {t}")

    # Current date: 2024-12-08
    # Add users
    users = [
        {'id':generate_id(),'username':'admin','password':hash_password('admin123'),'role':'admin'},
        {'id':generate_id(),'username':'manager','password':hash_password('manager123'),'role':'manager'},
        {'id':generate_id(),'username':'staff','password':hash_password('staff123'),'role':'staff'}
    ]
    for u in users:
        db.insert_record('users', u)

    # Cinemas in multiple cities
    cinema_data = [
        # Birmingham
        {'id':generate_id(),'city':'Birmingham','name':'Birmingham Cinema 1','location':'City Center'},
        {'id':generate_id(),'city':'Birmingham','name':'Birmingham Cinema 2','location':'High Street'},
        # Bristol
        {'id':generate_id(),'city':'Bristol','name':'Bristol Cinema 1','location':'Bristol Center'},
        {'id':generate_id(),'city':'Bristol','name':'Bristol Cinema 2','location':'Bristol Riverside'},
        # Cardiff
        {'id':generate_id(),'city':'Cardiff','name':'Cardiff Cinema 1','location':'Cardiff Bay'},
        {'id':generate_id(),'city':'Cardiff','name':'Cardiff Cinema 2','location':'Cardiff Center'},
        # London
        {'id':generate_id(),'city':'London','name':'London Cinema 1','location':'London West'},
        {'id':generate_id(),'city':'London','name':'London Cinema 2','location':'London East'}
    ]
    for c in cinema_data:
        db.insert_record('cinemas', c)

    # Films
    f1 = generate_id()
    f2 = generate_id()
    f3 = generate_id()
    films = [
        {'id':f1,'title':'Inception','genre':'Sci-Fi','rating':'12A','duration':148,'description':'A mind-bending thriller','actors':'Leonardo DiCaprio, Ellen Page'},
        {'id':f2,'title':'The Dark Knight','genre':'Action','rating':'12A','duration':152,'description':'Batman vs Joker','actors':'Christian Bale, Heath Ledger'},
        {'id':f3,'title':'Interstellar','genre':'Sci-Fi','rating':'12A','duration':169,'description':'Space journey','actors':'Matthew McConaughey, Anne Hathaway'}
    ]
    for film in films:
        db.insert_record('films', film)

    # Screens (just add to Bristol Cinema 1 and Birmingham Cinema 1 for example)
    c_bristol_1 = db.execute_query("SELECT id FROM cinemas WHERE name='Bristol Cinema 1'")[0][0]
    c_birm_1 = db.execute_query("SELECT id FROM cinemas WHERE name='Birmingham Cinema 1'")[0][0]

    s1 = generate_id()
    s2 = generate_id()
    s3 = generate_id()
    s4 = generate_id()

    screens = [
        {'id':s1,'screenNumber':'1','capacity':100,'type':'standard','cinema_id':c_bristol_1},
        {'id':s2,'screenNumber':'2','capacity':80,'type':'standard','cinema_id':c_bristol_1},
        {'id':s3,'screenNumber':'1','capacity':120,'type':'standard','cinema_id':c_birm_1},
        {'id':s4,'screenNumber':'2','capacity':60,'type':'standard','cinema_id':c_birm_1},
    ]
    for sc in screens:
        db.insert_record('screens', sc)

    # Sessions (one week advance from 2024-12-08 means <=2024-12-15)
    # Bristol sessions
    sess1 = generate_id()
    sess2 = generate_id()
    sess3 = generate_id()
    # Birmingham sessions
    sess4 = generate_id()
    sess5 = generate_id()
    sess6 = generate_id()

    sessions = [
        {'id':sess1,'sessionID':'S1','date':'2024-12-10','time':'10:00','filmId':f1,'screenId':s1,'city':'Bristol'},
        {'id':sess2,'sessionID':'S2','date':'2024-12-10','time':'14:00','filmId':f2,'screenId':s2,'city':'Bristol'},
        {'id':sess3,'sessionID':'S3','date':'2024-12-11','time':'19:00','filmId':f3,'screenId':s1,'city':'Bristol'},
        {'id':sess4,'sessionID':'S4','date':'2024-12-12','time':'10:00','filmId':f1,'screenId':s3,'city':'Birmingham'},
        {'id':sess5,'sessionID':'S5','date':'2024-12-12','time':'19:00','filmId':f2,'screenId':s4,'city':'Birmingham'},
        {'id':sess6,'sessionID':'S6','date':'2024-12-13','time':'14:00','filmId':f3,'screenId':s3,'city':'Birmingham'},
    ]
    for se in sessions:
        db.insert_record('sessions', se)

    # Add a booking for cancellation testing
    staff_id = db.execute_query("SELECT id FROM users WHERE username='staff'")[0][0]
    bk_id = generate_id()
    db.insert_record('bookings',{
        'id':bk_id,
        'bookingID':'TEST-CANCEL-001',
        'bookingDate':'2024-12-08',
        'date':'2024-12-10',
        'seats':2,
        'ticketType':'lower_hall',
        'userId':staff_id,
        'sessionId':sess1,
        'totalPrice':10.0
    })
