"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the main window interface of the cinema booking system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.film_listing import FilmListingScreen
from gui.booking_window import BookingScreen
from gui.cancellation_screen import CancellationScreen
from gui.film_management import FilmManagementScreen
from gui.reports_screen import ReportsScreen
from gui.cinema_management import CinemaManagementScreen

class MainWindow:
    def __init__(self,user_data,login_window):
        self.user_data=user_data
        self.login_window=login_window
        self.root=tk.Toplevel()
        self.root.title(f"HC Booking System - {user_data['role'].title()}")
        self.root.state('zoomed')
        self.create_gui()
        self.setup_menu()
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

    def create_gui(self):
        self.main_container=ttk.Frame(self.root,padding="10")
        self.main_container.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

        self.menu_panel=ttk.Frame(self.main_container,padding="10",relief="raised",borderwidth=1)
        self.menu_panel.grid(row=0,column=0,sticky=(tk.N,tk.S))

        self.content_area=ttk.Frame(self.main_container,padding="10")
        self.content_area.grid(row=0,column=1,sticky=(tk.W,tk.E,tk.N,tk.S))

        ttk.Label(self.content_area,text=f"Welcome, {self.user_data['username']}!",font=('Helvetica',16,'bold')).grid(row=0,column=0,pady=20)

    def setup_menu(self):
        # Common
        ttk.Button(self.menu_panel,text="Film Listings",command=self.show_film_listings).pack(fill=tk.X,pady=5)
        ttk.Button(self.menu_panel,text="Book Tickets",command=self.show_booking_screen).pack(fill=tk.X,pady=5)
        ttk.Button(self.menu_panel,text="Cancel Booking",command=self.show_cancellation_screen).pack(fill=tk.X,pady=5)

        # Admin & Manager
        if self.user_data['role'] in ['admin','manager']:
            ttk.Button(self.menu_panel,text="Manage Films/Screenings",command=self.show_film_management).pack(fill=tk.X,pady=5)
            ttk.Button(self.menu_panel,text="View Reports",command=self.show_reports).pack(fill=tk.X,pady=5)

        # Manager
        if self.user_data['role']=='manager':
            ttk.Button(self.menu_panel,text="Manage Cinemas",command=self.show_cinema_management).pack(fill=tk.X,pady=5)

        ttk.Separator(self.menu_panel).pack(fill=tk.X,pady=10)
        ttk.Button(self.menu_panel,text="Logout",command=self.logout).pack(fill=tk.X,pady=5)

    def clear_content_area(self):
        for w in self.content_area.winfo_children():
            w.destroy()

    def show_film_listings(self):
        self.clear_content_area()
        FilmListingScreen(self.content_area,self.user_data)

    def show_booking_screen(self):
        self.clear_content_area()
        BookingScreen(self.content_area,self.user_data)

    def show_cancellation_screen(self):
        self.clear_content_area()
        CancellationScreen(self.content_area,self.user_data)

    def show_film_management(self):
        self.clear_content_area()
        FilmManagementScreen(self.content_area,self.user_data)

    def show_reports(self):
        self.clear_content_area()
        ReportsScreen(self.content_area,self.user_data)

    def show_cinema_management(self):
        self.clear_content_area()
        CinemaManagementScreen(self.content_area,self.user_data)

    def logout(self):
        if messagebox.askyesno("Logout","Are you sure you want to logout?"):
            self.root.destroy()
            self.login_window.deiconify()

    def on_closing(self):
        if messagebox.askyesno("Quit","Are you sure you want to quit?"):
            self.root.destroy()
            self.login_window.destroy()

    def run(self):
        self.root.mainloop()
