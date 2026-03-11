import customtkinter as ctk
from PIL import Image
from tkinter import filedialog

# Set the theme to dark mode (matches your style!)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ShadowHideApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ShadowHide - Secure Image Steganography")
        self.geometry("500x400")

        # Title Label
        self.label = ctk.CTkLabel(self, text="ShadowHide", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # Encode Section
        self.encode_btn = ctk.CTkButton(self, text="Hide Message (Encode)", command=self.open_encode_view)
        self.encode_btn.pack(pady=10)

        # Decode Section
        self.decode_btn = ctk.CTkButton(self, text="Read Secret (Decode)", command=self.open_decode_view)
        self.decode_btn.pack(pady=10)

    def open_encode_view(self):
        input_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if not input_path: return

        dialog = ctk.CTkInputDialog(text="Enter the secret message to hide:", title="Encode Message")
        secret_text = dialog.get_input()
        if not secret_text: return

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not output_path: return

        if self.hide_message(input_path, secret_text, output_path):
            print(f"Success! Secret hidden in: {output_path}")
        else:
            print("Error: Image too small for this message.")

    def open_decode_view(self):
        file_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("PNG files", "*.png")])
        if not file_path: return

        secret_msg = self.reveal_message(file_path)
        
        result_window = ctk.CTkToplevel(self)
        result_window.title("Decoded Message")
        result_window.geometry("300x150")
        label = ctk.CTkLabel(result_window, text=f"The secret is:\n\n{secret_msg}", font=("Roboto", 14))
        label.pack(pady=30)

    def hide_message(self, image_path, message, output_path):
        img = Image.open(image_path).convert('RGB')
        encoded = img.copy()
        width, height = img.size
        message += "#####" 
        binary_msg = ''.join(format(ord(i), '08b') for i in message)
        data_index = 0
        for y in range(height):
            for x in range(width):
                pixel = list(img.getpixel((x, y)))
                for n in range(3): 
                    if data_index < len(binary_msg):
                        pixel[n] = pixel[n] & ~1 | int(binary_msg[data_index])
                        data_index += 1
                encoded.putpixel((x, y), tuple(pixel))
                if data_index >= len(binary_msg):
                    encoded.save(output_path)
                    return True
        return False

    def reveal_message(self, image_path):
        img = Image.open(image_path).convert('RGB')
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                for n in range(3):
                    binary_data += str(pixel[n] & 1)
        
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_msg = ""
        for byte in all_bytes:
            decoded_msg += chr(int(byte, 2))
            if decoded_msg[-5:] == "#####":
                return decoded_msg[:-5]
        return "No secret message found."

if __name__ == "__main__":
    app = ShadowHideApp()
    app.mainloop()