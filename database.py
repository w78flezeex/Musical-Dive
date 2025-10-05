import sqlite3
import os

DB_NAME = "users.db"

def init_db():
    if not os.path.exists(DB_NAME):
        print("Создание базы данных...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            full_name TEXT,
            age INTEGER,
            gender TEXT,
            instrument TEXT,
            about TEXT,
            city TEXT,
            latitude REAL,
            longitude REAL,
            video_file_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_registered BOOLEAN DEFAULT 0
        )
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            FOREIGN KEY (user_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user_id) REFERENCES users (tg_id),
            FOREIGN KEY (to_user_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter_id INTEGER NOT NULL,
            reported_user_id INTEGER NOT NULL,
            message_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending', -- 'pending', 'banned', 'dismissed'
            FOREIGN KEY (reporter_id) REFERENCES users (tg_id),
            FOREIGN KEY (reported_user_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS blacklist (
            user_id INTEGER PRIMARY KEY,
            reason TEXT,
            banned_by INTEGER,
            banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (tg_id),
            FOREIGN KEY (banned_by) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS last_city_shown (
            user_id INTEGER PRIMARY KEY,
            city TEXT,
            last_shown_user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (tg_id),
            FOREIGN KEY (last_shown_user_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS profile_moderation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
            moderator_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            moderated_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (tg_id),
            FOREIGN KEY (moderator_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS link_warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            warning_count INTEGER DEFAULT 0,
            last_warning TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (tg_id)
        )
        CREATE TABLE IF NOT EXISTS viewed_profiles (
            viewer_id INTEGER,
            viewed_id INTEGER,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (viewer_id, viewed_id),
            FOREIGN KEY (viewer_id) REFERENCES users (tg_id),
            FOREIGN KEY (viewed_id) REFERENCES users (tg_id)
        )
