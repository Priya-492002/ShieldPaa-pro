import customtkinter as ctk
import re        # Fixes the 're is not defined' error
import secrets   # Used for secure random generation
import string    # Used for character sets

class SecureVault(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Secure Vault - Password Suite")
        self.geometry("460x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Header
        self.label = ctk.CTkLabel(self, text="ShieldPass Pro", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # 1. Slider for Password Length
        self.length_label = ctk.CTkLabel(self, text="Password Length: 12")
        self.length_label.pack()
        self.length_slider = ctk.CTkSlider(self, from_=8, to=32, command=self.update_length_text)
        self.length_slider.set(12)
        self.length_slider.pack(pady=10)

        # 2. Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate Secure Password", command=self.generate_password)
        self.generate_button.pack(pady=10)

        # 3. Result Display
        self.result_entry = ctk.CTkEntry(self, placeholder_text="Result", width=300)
        self.result_entry.pack(pady=10)

        # 4. Strength Tester Input
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Test a password...", width=300)
        self.password_entry.pack(pady=10)
        
        # REAL-TIME BINDING: This triggers the check as you type
        self.password_entry.bind("<KeyRelease>", self.check_strength)

        # 5. Strength Label
        self.strength_label = ctk.CTkLabel(self, text="Strength: N/A", text_color="gray")
        self.strength_label.pack(pady=5)

    def update_length_text(self, value):
        """Updates the UI label to show the current slider value."""
        self.length_label.configure(text=f"Password Length: {int(value)}")

    def generate_password(self):
        """Generates a secure password based on the slider length."""
        length = int(self.length_slider.get())
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(secrets.choice(chars) for _ in range(length))
        
        self.result_entry.delete(0, "end")
        self.result_entry.insert(0, password)

    def check_strength(self, event=None):
        """Analyzes password strength in real-time."""
        password = self.password_entry.get()
        
        if not password:
            self.strength_label.configure(text="Strength: N/A", text_color="gray")
            return

        strength = 0
        if len(password) >= 8: strength += 1
        if any(char.isdigit() for char in password): strength += 1
        if any(char.isupper() for char in password): strength += 1
        if re.search(r"[!@#$%^&*]", password): strength += 1

        # Update UI colors
        if strength <= 1:
            self.strength_label.configure(text="Strength: Weak", text_color="red")
        elif strength == 2:
            self.strength_label.configure(text="Strength: Medium", text_color="orange")
        else:
            self.strength_label.configure(text="Strength: Strong", text_color="green")

if __name__ == "__main__":
    app = SecureVault()
    app.mainloop()