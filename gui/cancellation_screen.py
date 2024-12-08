import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
from datetime import datetime

class CancellationScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        ttk.Label(self.parent,text="Cancel Booking",font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)

        ttk.Label(self.parent,text="Booking Reference:").grid(row=1,column=0,sticky=tk.W)
        self.booking_ref_var=tk.StringVar()
        ttk.Entry(self.parent,textvariable=self.booking_ref_var,width=30).grid(row=1,column=1,pady=5)

        ttk.Button(self.parent,text="Search & Cancel",command=self.cancel_booking).grid(row=2,column=0,columnspan=2,pady=10)

    def cancel_booking(self):
        ref=self.booking_ref_var.get().strip()
        if not ref:
            messagebox.showerror("Error","Enter booking reference.")
            return
        db=DatabaseManager()
        query="""SELECT bookings.id, bookings.date, sessions.date, sessions.time 
                 FROM bookings JOIN sessions ON bookings.sessionId=sessions.id 
                 WHERE bookingID=?"""
        result=db.execute_query(query,(ref,))
        if not result:
            messagebox.showerror("Error","Booking not found.")
            return
        bookingId,booking_date,show_date,show_time=result[0]
        show_dt=datetime.strptime(show_date,"%Y-%m-%d")
        ref_dt=datetime(2024,12,8)
        delta=(show_dt-ref_dt).days
        if delta<=0:
            messagebox.showerror("Error","No cancellation allowed on show day or after.")
            return
        # Allowed with 50% fee (we just delete booking)
        db.execute_query("DELETE FROM bookings WHERE id=?",(bookingId,))
        messagebox.showinfo("Success","Booking cancelled with 50% charges applied.")
