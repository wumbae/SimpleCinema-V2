"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the booking interface of the cinema booking system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
import uuid
from datetime import datetime, timedelta

def get_base_price(city, time):
    prices = {
        'Birmingham': {'morning':5,'afternoon':5,'evening':6},
        'Bristol': {'morning':7,'afternoon':6,'evening':7},
        'Cardiff': {'morning':8,'afternoon':5,'evening':6},
        'London': {'morning':7,'afternoon':10,'evening':11}
    }
    hour=int(time.split(':')[0])
    if 8<=hour<12:
        slot='morning'
    elif 12<=hour<17:
        slot='afternoon'
    else:
        slot='evening'
    return prices[city][slot]

class BookingScreen:
    def __init__(self,parent,user_data):
        self.parent=parent
        self.user_data=user_data
        
        # Create main container frame
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create booking form frame (left side)
        booking_frame = ttk.Frame(main_frame)
        booking_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create receipt frame (right side)
        receipt_frame = ttk.LabelFrame(main_frame, text="Booking Receipt")
        receipt_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        # Add receipt placeholder
        self.receipt_text = tk.Text(receipt_frame, width=30, height=20)
        self.receipt_text.grid(padx=10, pady=10)
        self.receipt_text.config(state='disabled')

        # Move existing booking form elements to booking_frame instead of self.parent
        ttk.Label(booking_frame,text="Book Tickets",font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)

        self.city_var=tk.StringVar()
        self.film_var=tk.StringVar()
        self.date_var=tk.StringVar()
        self.time_var=tk.StringVar()
        self.ticket_type_var=tk.StringVar(value="lower_hall")
        self.tickets_var=tk.IntVar(value=1)

        cities=['Birmingham','Bristol','Cardiff','London']
        ttk.Label(booking_frame,text="City:").grid(row=1,column=0,sticky=tk.W)
        c_combo=ttk.Combobox(booking_frame,textvariable=self.city_var,values=cities,state='readonly')
        c_combo.grid(row=1,column=1,pady=5)

        ttk.Label(booking_frame,text="Film:").grid(row=2,column=0,sticky=tk.W)
        self.film_combo=ttk.Combobox(booking_frame,textvariable=self.film_var,state='readonly')
        self.film_combo.grid(row=2,column=1,pady=5)

        ttk.Label(booking_frame,text="Date:").grid(row=3,column=0,sticky=tk.W)
        self.date_combo=ttk.Combobox(booking_frame,textvariable=self.date_var,state='readonly')
        self.date_combo.grid(row=3,column=1,pady=5)

        ttk.Label(booking_frame,text="Time:").grid(row=4,column=0,sticky=tk.W)
        self.time_combo=ttk.Combobox(booking_frame,textvariable=self.time_var,state='readonly')
        self.time_combo.grid(row=4,column=1,pady=5)

        ttk.Label(booking_frame,text="Ticket Type:").grid(row=5,column=0,sticky=tk.W)
        ttk.Radiobutton(booking_frame,text="Lower Hall",value="lower_hall",variable=self.ticket_type_var).grid(row=5,column=1,sticky=tk.W)
        ttk.Radiobutton(booking_frame,text="Upper Gallery",value="upper_gallery",variable=self.ticket_type_var).grid(row=6,column=1,sticky=tk.W)
        ttk.Radiobutton(booking_frame,text="VIP",value="vip",variable=self.ticket_type_var).grid(row=7,column=1,sticky=tk.W)

        ttk.Label(booking_frame,text="Number of Tickets:").grid(row=8,column=0,sticky=tk.W)
        ttk.Spinbox(booking_frame,from_=1,to=10,textvariable=self.tickets_var).grid(row=8,column=1,pady=5)

        ttk.Button(booking_frame,text="Load Films",command=self.load_films).grid(row=9,column=0,pady=10)
        ttk.Button(booking_frame,text="Load Showtimes",command=self.load_showtimes).grid(row=9,column=1,pady=10)
        ttk.Button(booking_frame,text="Check Price & Availability",command=self.check_price).grid(row=10,column=0,pady=10)
        ttk.Button(booking_frame,text="Confirm Booking",command=self.confirm_booking).grid(row=10,column=1,pady=10)

        self.info_label=ttk.Label(booking_frame,text="")
        self.info_label.grid(row=11,column=0,columnspan=2)

    def load_films(self):
        city=self.city_var.get()
        if not city:
            messagebox.showerror("Error","Select a city first.")
            return
        db=DatabaseManager()
        res=db.execute_query("SELECT DISTINCT films.title FROM films JOIN sessions ON films.id=sessions.filmId WHERE sessions.city=?",(city,))
        if res:
            films=[r[0] for r in res]
            self.film_combo['values']=films
            if films:
                self.film_combo.set(films[0])

    def load_showtimes(self):
        city=self.city_var.get()
        film=self.film_var.get()
        if not film:
            messagebox.showerror("Error","Select a film.")
            return
        db=DatabaseManager()
        res=db.execute_query("SELECT DISTINCT date FROM sessions JOIN films ON films.id=sessions.filmId WHERE films.title=? AND city=?",(film,city))
        if res:
            dates=[r[0] for r in res]
            self.date_combo['values']=dates
            if dates:
                self.date_combo.set(dates[0])
            self.date_combo.bind('<<ComboboxSelected>>',self.update_times)

    def update_times(self,event=None):
        city=self.city_var.get()
        film=self.film_var.get()
        date=self.date_var.get()
        db=DatabaseManager()
        res=db.execute_query("SELECT time FROM sessions JOIN films ON films.id=sessions.filmId WHERE films.title=? AND city=? AND date=?",(film,city,date))
        if res:
            times=[r[0] for r in res]
            self.time_combo['values']=times
            if times:
                self.time_combo.set(times[0])

    def check_price(self):
        city=self.city_var.get()
        film=self.film_var.get()
        date=self.date_var.get()
        time=self.time_var.get()
        ttype=self.ticket_type_var.get()
        tickets=self.tickets_var.get()
        if not (city and film and date and time):
            messagebox.showerror("Error","Select all details.")
            return
        show_dt=datetime.strptime(date,"%Y-%m-%d")
        ref_dt=datetime(2024,12,8)
        if show_dt<ref_dt or show_dt>ref_dt+timedelta(days=7):
            messagebox.showerror("Error","Booking outside allowed range.")
            return
        if tickets<1:
            messagebox.showerror("Error","Must book at least 1 ticket.")
            return
        base=get_base_price(city,time)
        if ttype=='upper_gallery':
            base*=1.2
        elif ttype=='vip':
            base*=1.44
        total=base*tickets
        self.info_label.config(text=f"Seats available. Total Price: £{total:.2f}")

    def confirm_booking(self):
        city=self.city_var.get()
        film=self.film_var.get()
        date=self.date_var.get()
        time=self.time_var.get()
        ttype=self.ticket_type_var.get()
        tickets=self.tickets_var.get()
        if not (city and film and date and time):
            messagebox.showerror("Error","Check price first.")
            return
        db=DatabaseManager()
        sess=db.execute_query("""SELECT sessions.id FROM sessions 
                                 JOIN films ON films.id=sessions.filmId 
                                 WHERE films.title=? AND city=? AND date=? AND time=?""",(film,city,date,time))
        if not sess:
            messagebox.showerror("Error","No session found.")
            return
        sessionId=sess[0][0]
        base=get_base_price(city,time)
        if ttype=='upper_gallery':
            base*=1.2
        elif ttype=='vip':
            base*=1.44
        total=base*tickets
        booking_id=str(uuid.uuid4())
        data={
            'id':str(uuid.uuid4()),
            'bookingID':booking_id,
            'bookingDate':'2024-12-08',
            'date':date,
            'seats':tickets,
            'ticketType':ttype,
            'userId':self.user_data['id'],
            'sessionId':sessionId,
            'totalPrice':total
        }
        db.insert_record('bookings',data)
        messagebox.showinfo("Success",f"Booking confirmed!\nRef: {booking_id}\nTotal: £{total:.2f}")
        self.info_label.config(text="")
        
        # After successful booking, update the receipt
        self.update_receipt(booking_id, {
            'film': film,
            'date': date,
            'time': time,
            'screen': ttype.replace('_', ' ').title(),
            'tickets': tickets,
            'total': total,
            'booking_date': '2024-12-08'  # Current date in your system
        })

    def update_receipt(self, booking_id, details):
        """Update the receipt display with booking details"""
        receipt_text = f"""
        BOOKING REFERENCE: {booking_id}
        ------------------------
        Film: {details['film']}
        Date: {details['date']}
        Time: {details['time']}
        Screen: {details['screen']}
        Number of Tickets: {details['tickets']}
        ------------------------
        Total Cost: £{details['total']:.2f}
        ------------------------
        Booking Date: {details['date']}
        """
        
        self.receipt_text.config(state='normal')
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(1.0, receipt_text)
        self.receipt_text.config(state='disabled')
