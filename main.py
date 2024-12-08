"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the main functionality of the cinema booking system.
"""



from gui.login_window import LoginWindow
from database.db_config import initialize_database

def main():
    initialize_database()
    login = LoginWindow()
    login.run()

if __name__ == "__main__":
    main()
