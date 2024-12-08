"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the film management interface of the cinema booking system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
import uuid

class FilmManagementScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Film Management",font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)

        self.tree=ttk.Treeview(self.parent,columns=('Title','Genre','Age Rating','Movie Rating','Duration','Actors','Description'),show='headings',height=8)
        for col in ('Title','Genre','Age Rating','Movie Rating','Duration','Actors','Description'):
            self.tree.heading(col,text=col)
            if col in ['Title', 'Actors', 'Description']:
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        self.tree.grid(row=1,column=0,columnspan=2)

        ttk.Button(self.parent,text="Load Films",command=self.load_films).grid(row=2,column=0,pady=5)
        ttk.Button(self.parent,text="Delete Film",command=self.delete_film).grid(row=2,column=1,pady=5)

        ttk.Label(self.parent,text="Add/Update Film:").grid(row=3,column=0,columnspan=2,pady=10)
        ttk.Label(self.parent,text="Title:").grid(row=4,column=0,sticky=tk.W)
        self.title_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.title_var,width=30).grid(row=4,column=1,pady=5)

        ttk.Label(self.parent,text="Genre:").grid(row=5,column=0,sticky=tk.W)
        self.genre_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.genre_var,width=30).grid(row=5,column=1,pady=5)

        ttk.Label(self.parent,text="Age Rating:").grid(row=6,column=0,sticky=tk.W)
        self.age_rating_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.age_rating_var,width=30).grid(row=6,column=1,pady=5)

        ttk.Label(self.parent,text="Movie Rating:").grid(row=7,column=0,sticky=tk.W)
        self.movie_rating_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.movie_rating_var,width=30).grid(row=7,column=1,pady=5)

        ttk.Label(self.parent,text="Duration:").grid(row=8,column=0,sticky=tk.W)
        self.duration_var=tk.IntVar()
        ttk.Entry(self.parent,textvariable=self.duration_var,width=30).grid(row=8,column=1,pady=5)

        ttk.Label(self.parent,text="Actors:").grid(row=9,column=0,sticky=tk.W)
        self.actors_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.actors_var,width=30).grid(row=9,column=1,pady=5)

        ttk.Label(self.parent,text="Description:").grid(row=10,column=0,sticky=tk.W)
        self.description_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.description_var,width=30).grid(row=10,column=1,pady=5)

        ttk.Button(self.parent,text="Add Film",command=self.add_film).grid(row=11,column=0,columnspan=2,pady=10)

    def load_films(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        db=DatabaseManager()
        results=db.execute_query("SELECT title,genre,rating,movie_rating,duration,actors,description FROM films")
        if results:
            for r in results:
                self.tree.insert('',tk.END,values=r)

    def add_film(self):
        try:
            title = self.title_var.get().strip()
            genre = self.genre_var.get().strip()
            age_rating = self.age_rating_var.get().strip()
            movie_rating = self.movie_rating_var.get().strip()
            actors = self.actors_var.get().strip()
            description = self.description_var.get().strip()
            
            # Handle duration conversion safely
            try:
                duration = int(self.duration_var.get())
                if duration <= 0:
                    raise ValueError("Duration must be positive")
            except (ValueError, tk.TclError):
                messagebox.showerror("Error", "Duration must be a positive number")
                return
            
            if not (title and genre and age_rating):
                messagebox.showerror("Error", "Please fill all required fields (Title, Genre, Age Rating, Duration)")
                return
                
            db = DatabaseManager()
            data = {
                'id': str(uuid.uuid4()),
                'title': title,
                'genre': genre,
                'rating': age_rating,
                'movie_rating': movie_rating,
                'duration': duration,
                'description': description,
                'actors': actors
            }
            
            db.insert_record('films', data)
            
            # Clear the form after successful addition
            self.title_var.set('')
            self.genre_var.set('')
            self.age_rating_var.set('')
            self.movie_rating_var.set('')
            self.duration_var.set('')
            self.actors_var.set('')
            self.description_var.set('')
            
            messagebox.showinfo("Success", "Film added successfully!")
            self.load_films()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add film: {str(e)}")

    def delete_film(self):
        selection=self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning","Select a film to delete.")
            return
        film_title=self.tree.item(selection[0])['values'][0]
        db=DatabaseManager()
        fid=db.execute_query("SELECT id FROM films WHERE title=?",(film_title,))
        if fid:
            db.execute_query("DELETE FROM films WHERE id=?",(fid[0][0],))
            messagebox.showinfo("Success","Film deleted.")
            self.load_films()
