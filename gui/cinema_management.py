import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
import uuid

class CinemaManagementScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Cinema Management",font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)

        self.cinema_tree=ttk.Treeview(self.parent,columns=('Name','Location','City'),show='headings')
        self.cinema_tree.heading('Name',text='Name')
        self.cinema_tree.heading('Location',text='Location')
        self.cinema_tree.heading('City',text='City')
        self.cinema_tree.grid(row=1,column=0,columnspan=2)

        ttk.Button(self.parent,text="Load Cinemas",command=self.load_cinemas).grid(row=2,column=0,pady=5)
        ttk.Button(self.parent,text="Delete Cinema",command=self.delete_cinema).grid(row=2,column=1,pady=5)

        ttk.Label(self.parent,text="Add New Cinema:").grid(row=3,column=0,columnspan=2,pady=10)
        ttk.Label(self.parent,text="City:").grid(row=4,column=0,sticky=tk.W)
        self.city_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.city_var,width=30).grid(row=4,column=1,pady=5)

        ttk.Label(self.parent,text="Name:").grid(row=5,column=0,sticky=tk.W)
        self.cname_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.cname_var,width=30).grid(row=5,column=1,pady=5)

        ttk.Label(self.parent,text="Location:").grid(row=6,column=0,sticky=tk.W)
        self.clocation_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.clocation_var,width=30).grid(row=6,column=1,pady=5)

        ttk.Button(self.parent,text="Add Cinema",command=self.add_cinema).grid(row=7,column=0,columnspan=2,pady=10)

    def load_cinemas(self):
        for i in self.cinema_tree.get_children():
            self.cinema_tree.delete(i)
        db=DatabaseManager()
        res=db.execute_query("SELECT name, location, city FROM cinemas")
        if res:
            for r in res:
                self.cinema_tree.insert('',tk.END,values=r)

    def add_cinema(self):
        city=self.city_var.get().strip()
        name=self.cname_var.get().strip()
        loc=self.clocation_var.get().strip()
        if not (city and name and loc):
            messagebox.showerror("Error","Provide city, name and location.")
            return
        db=DatabaseManager()
        data={
            'id':str(uuid.uuid4()),
            'city':city,
            'name':name,
            'location':loc
        }
        db.insert_record('cinemas',data)
        messagebox.showinfo("Success","Cinema added.")
        self.load_cinemas()

    def delete_cinema(self):
        selection=self.cinema_tree.selection()
        if not selection:
            messagebox.showwarning("Warning","Select a cinema to delete.")
            return
        cname=self.cinema_tree.item(selection[0])['values'][0]
        db=DatabaseManager()
        cid=db.execute_query("SELECT id FROM cinemas WHERE name=?",(cname,))
        if cid:
            db.execute_query("DELETE FROM cinemas WHERE id=?",(cid[0][0],))
            messagebox.showinfo("Success","Cinema deleted.")
            self.load_cinemas()
