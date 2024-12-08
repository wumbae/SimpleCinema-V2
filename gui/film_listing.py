import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager

class FilmListingScreen:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        
        ttk.Label(self.parent, text="Film Listings", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, pady=20)

        columns = (
            "Title", "Genre", "Movie Rating", "Duration",
            "Actors", "Description", "City", "Date", "Time",
            "Available Seats"
        )
        
        self.tree_frame = ttk.Frame(self.parent)
        self.tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tree_scroll_y = ttk.Scrollbar(self.tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(
            self.tree_frame, 
            columns=columns, 
            show='headings', 
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ["Title", "Description", "Actors"]:
                self.tree.column(col, width=150)
            elif col in ["City", "Date", "Time"]:
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=80)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Execute the query
        db = DatabaseManager()
        query = """SELECT 
            films.title, 
            films.genre, 
            films.movie_rating,
            films.duration, 
            films.actors,
            films.description,
            sessions.city, 
            sessions.date, 
            sessions.time,
            (screens.capacity - COALESCE(SUM(bookings.seats), 0)) AS available_seats
        FROM films 
        JOIN sessions ON films.id = sessions.filmId
        JOIN screens ON sessions.screenId = screens.id
        LEFT JOIN bookings ON sessions.id = bookings.sessionId
        GROUP BY 
            films.title, 
            films.genre, 
            films.movie_rating, 
            films.duration, 
            films.actors, 
            films.description, 
            sessions.city, 
            sessions.date, 
            sessions.time"""
        
        results = db.execute_query(query)
        if results:
            for r in results:
                self.tree.insert('', tk.END, values=r)