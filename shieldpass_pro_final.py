import customtkinter as ctk
import random
import string

# Initialize the window
ctk.set_appearance_mode("Dark")
app = ctk.CTk()
app.geometry("400x500")
app.title("ShieldPass Pro - Real Time")

# --- Logic Functions ---

def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(int(length)))
    result_entry.delete(0, 'end')
    result_entry.insert(0, password)
    check_strength(password)

def slider_event(value):
    # Update the label text as you slide
    length_label.configure(text=f"Password Length: {int(value)}")
    # Generate new password instantly
    generate_password(value)

def check_strength(password):
    # Dynamic strength logic
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if length < 8:
        strength_label.configure(text="Strength: Weak", text_color="#FF5555")
    elif length < 14 or not (has_upper and has_digit):
        strength_label.configure(text="Strength: Medium", text_color="#FFB86C")
    else:
        strength_label.configure(text="Strength: Strong", text_color="#50FA7B")

def on_type(event):
    # Check strength as you type in the "Test" box
    check_strength(test_entry.get())

# --- UI Elements ---

title = ctk.CTkLabel(app, text="ShieldPass Pro", font=("Arial", 24, "bold"))
title.pack(pady=20)

# Slider Section
length_label = ctk.CTkLabel(app, text="Password Length: 12", font=("Arial", 14))
length_label.pack(pady=5)

slider = ctk.CTkSlider(app, from_=6, to=32, command=slider_event)
slider.set(12) # Default value
slider.pack(pady=10)

# Result Box
result_entry = ctk.CTkEntry(app, width=300, justify="center", placeholder_text="Result")
result_entry.pack(pady=20)

# Manual Test Box
test_label = ctk.CTkLabel(app, text="Test a password...", font=("Arial", 12))
test_label.pack(pady=(20, 0))

test_entry = ctk.CTkEntry(app, width=300, placeholder_text="Type here to test strength...")
test_entry.pack(pady=5)
# This "bind" makes it real-time as you type
test_entry.bind("<KeyRelease>", on_type) 

# Strength Display
strength_label = ctk.CTkLabel(app, text="Strength: N/A", font=("Arial", 14, "bold"))
strength_label.pack(pady=20)

app.mainloop()