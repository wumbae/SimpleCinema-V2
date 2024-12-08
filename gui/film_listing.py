import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager

class FilmListingScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Film Listings",font=('Helvetica',16,'bold')).grid(row=0,column=0,pady=20)

        columns=("Title","Genre","Rating","Duration","City","Date","Time")
        self.tree=ttk.Treeview(self.parent,columns=columns,show='headings')
        for col in columns:
            self.tree.heading(col,text=col)
        self.tree.grid(row=1,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

        db=DatabaseManager()
        q="""SELECT films.title, films.genre, films.rating, films.duration, sessions.city, sessions.date, sessions.time
             FROM films JOIN sessions ON films.id=sessions.filmId"""
        results=db.execute_query(q)
        if results:
            for r in results:
                self.tree.insert('',tk.END,values=r)
