"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module provides database management functionality for the cinema booking system.
"""

import sqlite3
from database.db_config import get_connection

class DatabaseManager:
    @staticmethod
    def execute_query(query, params=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def insert_record(table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        return DatabaseManager.execute_query(query, tuple(data.values()))
