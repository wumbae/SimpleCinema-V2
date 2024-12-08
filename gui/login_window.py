import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
from gui.main_window import MainWindow
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HC Booking System - Login")

        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Horizon Cinemas", font=('Helvetica',16,'bold')).grid(row=0,column=0,columnspan=2,pady=20)
        ttk.Label(main_frame,text="Username:").grid(row=1,column=0,sticky=tk.W,pady=5)
        self.username_var=tk.StringVar()
        self.username_entry=ttk.Entry(main_frame,textvariable=self.username_var,width=30)
        self.username_entry.grid(row=1,column=1,pady=5)

        ttk.Label(main_frame,text="Password:").grid(row=2,column=0,sticky=tk.W,pady=5)
        self.password_var=tk.StringVar()
        self.password_entry=ttk.Entry(main_frame,textvariable=self.password_var,show="*",width=30)
        self.password_entry.grid(row=2,column=1,pady=5)

        ttk.Label(main_frame,text="Role:").grid(row=3,column=0,sticky=tk.W,pady=5)
        self.role_var=tk.StringVar(value="staff")
        roles=[("Booking Staff","staff"),("Admin","admin"),("Manager","manager")]
        col_offset=1
        for text,val in roles:
            ttk.Radiobutton(main_frame,text=text,value=val,variable=self.role_var).grid(row=3,column=col_offset,sticky=tk.W)
            col_offset+=1

        ttk.Button(main_frame,text="Login",command=self.login).grid(row=4,column=0,columnspan=2,pady=20)
        self.root.bind('<Return>',lambda e:self.login())

    def login(self):
        username=self.username_var.get().strip()
        password=self.password_var.get().strip()
        role=self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error","Please enter both username and password")
            return

        db=DatabaseManager()
        # Get user by username and role
        res=db.execute_query("SELECT * FROM users WHERE username=? AND role=?",(username,role))
        if res:
            stored_hash=res[0][2]
            if stored_hash==hash_password(password):
                user_data={'id':res[0][0],'username':res[0][1],'role':res[0][3]}
                self.root.withdraw()
                mw=MainWindow(user_data,self.root)
                mw.run()
            else:
                messagebox.showerror("Error","Invalid password")
        else:
            messagebox.showerror("Error","Invalid credentials")

    def run(self):
        self.root.mainloop()
