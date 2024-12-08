import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
import uuid

class FilmManagementScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Film Management",font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)

        self.tree=ttk.Treeview(self.parent,columns=('Title','Genre','Rating','Duration'),show='headings',height=8)
        for col in ('Title','Genre','Rating','Duration'):
            self.tree.heading(col,text=col)
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

        ttk.Label(self.parent,text="Rating:").grid(row=6,column=0,sticky=tk.W)
        self.rating_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.rating_var,width=30).grid(row=6,column=1,pady=5)

        ttk.Label(self.parent,text="Duration:").grid(row=7,column=0,sticky=tk.W)
        self.duration_var=tk.IntVar()
        ttk.Entry(self.parent,textvariable=self.duration_var,width=30).grid(row=7,column=1,pady=5)

        ttk.Button(self.parent,text="Add Film",command=self.add_film).grid(row=8,column=0,columnspan=2,pady=10)

    def load_films(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        db=DatabaseManager()
        results=db.execute_query("SELECT title,genre,rating,duration FROM films")
        if results:
            for r in results:
                self.tree.insert('',tk.END,values=r)

    def add_film(self):
        title=self.title_var.get().strip()
        genre=self.genre_var.get().strip()
        rating=self.rating_var.get().strip()
        duration=self.duration_var.get()
        if not (title and genre and rating and duration):
            messagebox.showerror("Error","Please fill all fields")
            return
        db=DatabaseManager()
        data={
            'id':str(uuid.uuid4()),
            'title':title,
            'genre':genre,
            'rating':rating,
            'duration':duration,
            'description':'',
            'actors':''
        }
        db.insert_record('films',data)
        messagebox.showinfo("Success","Film added.")
        self.load_films()

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
