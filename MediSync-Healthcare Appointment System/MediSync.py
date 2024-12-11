import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3

bg_left = "#003366"
bg_right = "#FFFFFF"
label_fg = "#FFFFFF"
button_bg = "#FFFFFF"
button_fg = "#003366"

def init_db():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_date TEXT,
        appointment_time TEXT,
        patient_name TEXT,
        age INTEGER,
        sex TEXT,
        address TEXT,
        contact TEXT,       
        email TEXT,
        reason_for_visit TEXT,
        selected_doctor TEXT
    )
''')
    conn.commit()
    conn.close()

init_db()

appointments = []

root = tk.Tk()
root.title("MediSync Healthcare Appointment System")
root.geometry("800x450")
root.resizable(False, False)

left_frame = tk.Frame(root, bg=bg_left, width=400, height=450)
left_frame.pack(side="left", fill="both")

right_frame = tk.Frame(root, bg=bg_right, width=400, height=450)
right_frame.pack(side="right", fill="both")

def toggle_password(entry1, entry2, show_password_var):
    if show_password_var.get():
        entry1.config(show="")
        entry2.config(show="")
    else:
        entry1.config(show="*")
        entry2.config(show="*")

def show_main_menu():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Main Menu", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).pack(pady=20)

    menu_buttons = [
        ("Schedule Appointment", show_doctor_schedule),
        ("Update Appointment", show_update_appointment),
        ("View All Appointments", view_appointments),
        ("Cancel Appointment", show_cancel_appointment),
        ("Exit", root.destroy)
    ]

    for text, command in menu_buttons:
        tk.Button(left_frame, text=text, bg=button_bg, fg=button_fg, width=56, command=command).pack(pady=10)

def show_register():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Register", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).place(x=50, y=60)

    username_entry = tk.Entry(left_frame, width=30)
    username_entry.place(x=50, y=133)
    tk.Label(left_frame, text="Username", font=("Helvetica", 10), fg=label_fg, bg=bg_left).place(x=50, y=110)

    password_entry = tk.Entry(left_frame, width=30, show="*")
    password_entry.place(x=50, y=185)
    tk.Label(left_frame, text="Password", font=("Helvetica", 10), fg=label_fg, bg=bg_left).place(x=50, y=160)

    confirm_password_entry = tk.Entry(left_frame, width=30, show="*")
    confirm_password_entry.place(x=50, y=240)
    tk.Label(left_frame, text="Confirm Password", font=("Helvetica", 10), fg=label_fg, bg=bg_left).place(x=50, y=210)

    show_password_var = tk.BooleanVar()

    tk.Checkbutton(left_frame, text="Show Password", variable=show_password_var,
                   bg=bg_left, fg=label_fg, font=("Helvetica", 8),
                   command=lambda: toggle_password(password_entry, confirm_password_entry, show_password_var)).place(x=50, y=265)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            show_login()
        conn.close()

    tk.Button(left_frame, text="Register", bg=button_bg, fg=button_fg, width=10, command=register_user).place(x=50, y=295)
    tk.Label(left_frame, text="Already have an account?", font=("Helvetica", 8), fg=label_fg, bg=bg_left).place(x=50, y=325)

    clickable_login = tk.Label(left_frame, text="Login", font=("Helvetica", 8, "bold", "underline"),
                                fg="lightblue", bg=bg_left, cursor="hand2")
    clickable_login.place(x=181, y=325)
    clickable_login.bind("<Button-1>", lambda e: show_login())

def show_login():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Login", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).place(x=50, y=50)

    username_entry = tk.Entry(left_frame, width=30)
    username_entry.place(x=50, y=120)
    tk.Label(left_frame, text="Username", font=("Helvetica", 10), fg=label_fg, bg=bg_left).place(x=50, y=95)

    password_entry = tk.Entry(left_frame, width=30, show="*")
    password_entry.place(x=50, y=170)
    tk.Label(left_frame, text="Password", font=("Helvetica", 10), fg=label_fg, bg=bg_left).place(x=50, y=140)

    show_password_var = tk.BooleanVar()

    tk.Checkbutton(left_frame, text="Show Password", variable=show_password_var,
                   bg=bg_left, fg=label_fg, font=("Helvetica", 8),
                   command=lambda: toggle_password(password_entry, password_entry, show_password_var)).place(x=50, y=200)

    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        if cursor.fetchone():
            messagebox.showinfo("Success", f"Welcome to MediSync, {username}!")
            show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
        conn.close()

    tk.Button(left_frame, text="Login", bg=button_bg, fg=button_fg, width=10, command=login_user).place(x=50, y=230)
    tk.Label(left_frame, text="Don't have an account?", font=("Helvetica", 8), fg=label_fg, bg=bg_left).place(x=50, y=270)

    clickable_register = tk.Label(left_frame, text="Register", font=("Helvetica", 8, "bold", "underline"),
                                   fg="lightblue", bg=bg_left, cursor="hand2")
    clickable_register.place(x=167, y=270)
    clickable_register.bind("<Button-1>", lambda e: show_register())

try:
    logo_img = Image.open("image.png")
    logo_img = logo_img.resize((400, 400))
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(right_frame, image=logo_img, bg=bg_right)
    logo_label.place(x=5, y=5)
    logo_label.image = logo_img
except Exception as e:
    print(f"Error loading logo image: {e}")

def show_doctor_schedule():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Select a Doctor and Schedule Appointment", font=("Helvetica", 12, "bold"), fg=label_fg, bg=bg_left).pack(pady=20)

    table_frame = tk.Frame(left_frame, bg="#ffffff", relief="solid", bd=2, padx=20, pady=20)
    table_frame.pack(padx=30, pady=10, fill="both", expand=True)

    columns = ("No.", "Specialty", "Doctor", "Schedule")
    tree = ttk.Treeview(
        table_frame, columns=columns, show="headings", height=2, selectmode="browse"
    )

    style = ttk.Style()
    style.configure(
        "Treeview.Heading",
        font=("Arial", 11, "bold"),
        background="#f2f6fc",
        foreground="#004080"
    )
    style.configure(
        "Treeview",
        font=("Arial", 8),
        rowheight=30,
        background="#ffffff",
        foreground="black",
        fieldbackground="#f9f9f9"
    )

    for col in columns:
        tree.heading(col, text=col)

    tree.column("No.", width=65, anchor="center")
    tree.column("Specialty", width=185, anchor="center")
    tree.column("Doctor", width=155, anchor="center")
    tree.column("Schedule", width=288, anchor="w") 

    doctor_data = [
        ("1", "Primary Care Physician", "Dr. Maria Santos", "Mon-Fri 9:00 AM - 5:00 PM, Sat 9:00 AM - 12:00 PM"),
        ("2", "Dermatologist", "Dr. Juan de la Cruz", "Wed, Fri 10:00 AM - 6:00 PM, Sat 9:00 AM - 1:00 PM"),
        ("3", "Cardiologist", "Dr. Carlos Ramos", "Thu 8:00 AM - 4:00 PM, Tue, Fri 9:00 AM - 3:00 PM"),
        ("4", "Pediatrician", "Dr. Anabelle Garcia", "Mon-Fri 8:30 AM - 5:00 PM"),
        ("5", "Gynecologist", "Dr. Lara Reyes", "Fri 9:00 AM - 4:30 PM, Thu 10:00 AM - 6:00 PM"),
    ]

    for row in doctor_data:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)

    def schedule_selected_appointment():
        selected_item = tree.selection()
        if selected_item:
            selected_doctor = tree.item(selected_item, "values")[2]
            show_patient_information_form(selected_doctor) 
        else:
            messagebox.showwarning("No Selection", "Please select a doctor first.")

    tk.Button(left_frame, text="Schedule Appointment", bg=button_bg, fg=button_fg, width=30, command=schedule_selected_appointment).pack(pady=10)
    tk.Button(left_frame, text="Back", bg=button_bg, fg=button_fg, width=30, command=show_main_menu).pack(pady=10)

def show_patient_information_form(selected_doctor):
    for widget in left_frame.winfo_children():
        widget.destroy()

    patient_form_frame = tk.Frame(left_frame, bg=bg_left, width=50, height=50)
    patient_form_frame.pack_propagate(False) 
    patient_form_frame.pack(padx=45, pady=2, fill="both", expand=True)

    tk.Label(patient_form_frame, text="PATIENT INFORMATION", font=("Arial", 10, "bold"), fg=label_fg, bg=bg_left).grid(row=0, column=0, columnspan=2, pady=10)

    fields = [
        "Appointment Date", "Appointment Time", "Patient Name",
        "Age", "Sex", "Address", "Contact",
        "Email", "Reason for Visit"
    ]

    entries = {}

    for idx, field in enumerate(fields, start=1):
        label = tk.Label(patient_form_frame, text=field, font=("Arial", 8), fg=label_fg, bg=bg_left, anchor="w")
        label.grid(row=idx, column=0, sticky="w", padx=10, pady=8)

        entry = tk.Entry(patient_form_frame, font=("Arial", 8), width=30)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field] = entry  

    def submit_form():
        data = {field: entry.get() for field, entry in entries.items()}
        data["Selected Doctor"] = selected_doctor
        
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (appointment_date, appointment_time, patient_name, age, sex, address, contact, email, reason_for_visit, selected_doctor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data["Appointment Date"], data["Appointment Time"], data["Patient Name"], data["Age"], data["Sex"], 
              data["Address"], data["Contact"], data["Email"], data["Reason for Visit"], data["Selected Doctor"]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Form Submitted", f"Appointment scheduled with {selected_doctor}")
        show_main_menu()

    submit_button = tk.Button(patient_form_frame, text="Submit", bg=button_bg, fg=button_fg, width=10, command=submit_form)
    submit_button.grid(row=len(fields) + 1, column=0, padx=10, pady=5, sticky="e")

    back_button = tk.Button(patient_form_frame, text="Back", bg=button_bg, fg=button_fg, width=10, command=show_doctor_schedule)
    back_button.grid(row=len(fields) + 1, column=1, padx=10, pady=5, sticky="w")

def show_update_appointment():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(
        left_frame, text="Update Appointment", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left
    ).pack(pady=20)

    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments')
    appointments = cursor.fetchall()
    conn.close()

    if not appointments:
        tk.Label(
            left_frame, text="No appointments to update.", fg="gray", bg=bg_left
        ).pack(pady=20)
        tk.Button(
            left_frame, text="Back", bg=button_bg, fg=button_fg, width=56, command=show_main_menu
        ).pack(pady=10)
        return

    list_frame = tk.Frame(left_frame, bg="#ffffff", relief="solid", bd=2, padx=20, pady=20)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)

    tk.Label(
        list_frame,
        text="Select a patient to update their appointment:",
        font=("Arial", 10, "bold"),
        bg="#ffffff",
        fg="#004080",
    ).pack(anchor="w", pady=5)

    listbox = tk.Listbox(
        list_frame, font=("Arial", 10), width=60, height=10, selectmode="single", bg="#f9f9f9", fg="#333333"
    )
    listbox.pack(padx=20, pady=10, fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    for idx, appointment in enumerate(appointments):
        display_text = f"{appointment[3]}" 
        listbox.insert(idx, display_text)

    def edit_selected_patient():
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_appointment = appointments[selected_index]
            show_edit_appointment_form(selected_appointment)
        else:
            messagebox.showwarning("No Selection", "Please select a patient to update.")

    button_frame = tk.Frame(left_frame, bg=bg_left)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Edit Selected Patient",
        bg=button_bg,
        fg=button_fg,
        width=30,
        command=edit_selected_patient,
    ).pack(side="left", padx=5)

    tk.Button(
        button_frame, text="Back", bg=button_bg, fg=button_fg, width=20, command=show_main_menu
    ).pack(side="right", padx=10)
    
def show_edit_appointment_form(appointment):
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Edit Appointment", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).pack(pady=5)

    scroll_canvas = tk.Canvas(left_frame, bg=bg_left)
    scroll_frame = tk.Frame(scroll_canvas, bg=bg_left)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scroll_window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def update_scroll_region(event=None):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scroll_frame.bind("<Configure>", update_scroll_region)

    fields = [
        "Appointment Date", "Appointment Time", "Patient Name",
        "Age", "Sex", "Address", "Contact",
        "Email", "Reason for Visit"
    ]

    entries = {}
    for field, value in zip(fields, appointment[1:]):
        label = tk.Label(scroll_frame, text=field, font=("Arial", 10), fg=label_fg, bg=bg_left)
        label.pack(anchor="w", padx=80, pady=2)

        entry = tk.Entry(scroll_frame, font=("Arial", 10), width=52)
        entry.pack(padx=20, pady=5)
        entry.insert(0, value)
        entries[field] = entry

    # Doctor selection dropdown
    doctor_label = tk.Label(scroll_frame, text="Select Doctor", font=("Arial", 10), fg=label_fg, bg=bg_left)
    doctor_label.pack(anchor="w", padx=80, pady=2)

    doctor_combo = ttk.Combobox(scroll_frame, font=("Arial", 10), width=52)
    doctor_combo.pack(padx=20, pady=5)
    doctor_combo["values"] = [
        "Dr. Maria Santos - Primary Care Physician", 
        "Dr. Juan de la Cruz - Dermatologist", 
        "Dr. Carlos Ramos - Cardiologist", 
        "Dr. Anabelle Garcia - Pediatrician", 
        "Dr. Lara Reyes - Gynecologist"
    ]
    doctor_combo.set(appointment[10])  # Set the selected doctor based on the existing appointment

    def validate_and_save():
        updated_data = {field: entry.get().strip() for field, entry in entries.items()}
        updated_data["Selected Doctor"] = doctor_combo.get()

        missing_fields = [field for field, value in updated_data.items() if not value]

        if missing_fields:
            messagebox.showerror("Validation Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
            return

        if not validate_email(updated_data["Email"]):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return

        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            UPDATE appointments SET
                appointment_date = ?, appointment_time = ?, patient_name = ?, age = ?, sex = ?, 
                address = ?, contact = ?, email = ?, reason_for_visit = ?, selected_doctor = ?
            WHERE id = ?
        ''', (updated_data["Appointment Date"], updated_data["Appointment Time"], updated_data["Patient Name"], 
              updated_data["Age"], updated_data["Sex"], updated_data["Address"], updated_data["Contact"], 
              updated_data["Email"], updated_data["Reason for Visit"], updated_data["Selected Doctor"], appointment[0]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Appointment for {updated_data['Patient Name']} updated successfully!")
        show_update_appointment()

    def validate_email(email):
        import re
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    button_frame = tk.Frame(scroll_frame, bg=bg_left)
    button_frame.pack(pady=5)

    save_button = tk.Button(button_frame, text="Save Changes", bg=button_bg, fg=button_fg, width=20, command=validate_and_save)
    save_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", bg=button_bg, fg=button_fg, width=20, command=show_update_appointment)
    cancel_button.pack(side="left", padx=10)

    scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(scroll_window, width=e.width))

def view_appointments():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="All Appointments", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).pack(pady=20, padx=117)

    def fetch_appointments():
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments')
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    appointments = fetch_appointments()

    if not appointments:
        messagebox.showinfo("No Appointments", "No appointments found!")
        show_main_menu()
        return

    appointments_listbox = tk.Listbox(left_frame, width=67, height=15)
    appointments_listbox.pack(pady=10)
    for app in appointments:
        appointments_listbox.insert(tk.END, f"ID: {app[0]} | Doctor: {app[10]} | Name: {app[3]} | Date: {app[1]} | Sex: {app[5]} | Address: {app[6]} | Contact Number: {app[7]} | Email: {app[8]} | Reason for Visit: {app[9]}")

    tk.Button(left_frame, text="Back", bg=button_bg, fg=button_fg, width=20, command=show_main_menu).pack(pady=10)

def show_cancel_appointment():
    for widget in left_frame.winfo_children():
        widget.destroy()

    tk.Label(left_frame, text="Cancel Appointment", font=("Helvetica", 14, "bold"), fg=label_fg, bg=bg_left).pack(pady=20, padx=102)

    def fetch_appointments():
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments')
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    appointments = fetch_appointments()

    if not appointments:
        messagebox.showinfo("No Appointments", "No appointments found!")
        show_main_menu()
        return

    appointment_ids = [str(a[0]) for a in appointments]
    
    tk.Label(left_frame, text="Select Appointment ID", font=("Helvetica", 10), fg=label_fg, bg=bg_left).pack(pady=5)

    selected_appointment = ttk.Combobox(left_frame, values=appointment_ids, width=64, state="readonly")
    selected_appointment.pack(pady=10)

    def cancel_appointment():
        appointment_id = selected_appointment.get()

        if not appointment_id:
            messagebox.showwarning("Input Error", "Please select an appointment ID!")
            return

        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id=?', (appointment_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Appointment ID {appointment_id} has been canceled.")
        show_main_menu()

    cancel_button = tk.Button(left_frame, text="Cancel Appointment", bg=button_bg, fg=button_fg, width=20, command=cancel_appointment)
    cancel_button.pack(pady=30)
    back_button = tk.Button(left_frame, text="Back", bg=button_bg, fg=button_fg, width=20, command=show_main_menu)
    back_button.pack(pady=1)
    
show_login()
root.mainloop()