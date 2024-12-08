from gui.login_window import LoginWindow
from database.db_config import initialize_database

def main():
    initialize_database()
    login = LoginWindow()
    login.run()

if __name__ == "__main__":
    main()
