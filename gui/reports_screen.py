"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the reports interface of the cinema booking system.
"""

import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager

class ReportsScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Reports",font=('Helvetica',16,'bold')).grid(row=0,column=0,pady=20)

        ttk.Button(self.parent,text="Show Revenue Report",command=self.show_revenue).grid(row=1,column=0,pady=10)
        self.report_area=tk.Text(self.parent,width=50,height=10)
        self.report_area.grid(row=2,column=0,pady=10)

    def show_revenue(self):
        self.report_area.delete('1.0',tk.END)
        db=DatabaseManager()
        query="""SELECT films.title, SUM(bookings.totalPrice) as rev
                 FROM bookings
                 JOIN sessions ON bookings.sessionId=sessions.id
                 JOIN films ON sessions.filmId=films.id
                 GROUP BY films.title
                 ORDER BY rev DESC"""
        results=db.execute_query(query)
        if results:
            self.report_area.insert(tk.END,"Film Revenue:\n")
            for r in results:
                self.report_area.insert(tk.END,f"{r[0]}: £{r[1]:.2f}\n")
        else:
            self.report_area.insert(tk.END,"No bookings found.")
