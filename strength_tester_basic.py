import customtkinter as ctk
import re  # Fixed: Added the missing import to solve the error
import secrets
import string

class SecureVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Vault - Password Suite")
        self.geometry("460x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="ShieldPass Pro", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Password Entry (Where you type to test)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Test a password...", width=300)
        self.password_entry.pack(pady=10)
        
        # This line links your typing to the strength checker in real-time
        self.password_entry.bind("<KeyRelease>", self.check_strength)

        # Strength Label
        self.strength_label = ctk.CTkLabel(self, text="Strength: N/A", text_color="gray")
        self.strength_label.pack(pady=5)

    def check_strength(self, event=None):
        password = self.password_entry.get()
        
        if not password:
            self.strength_label.configure(text="Strength: N/A", text_color="gray")
            
            

        # Scoring Logic
        strength = 0
        if len(password) >= 8: strength += 1
        if any(char.isdigit() for char in password): strength += 1
        if any(char.isupper() for char in password): strength += 1
        if re.search(r"[!@#$%^&*]", password): strength += 1

        # Final Step: Update UI colors based on score
        if strength <= 1:
            self.strength_label.configure(text="Strength: Weak", text_color="red")
        elif strength == 2:
            self.strength_label.configure(text="Strength: Medium", text_color="orange")
        else:
            self.strength_label.configure(text="Strength: Strong", text_color="green")

if __name__ == "__main__":
    app = SecureVault()
    app.mainloop()