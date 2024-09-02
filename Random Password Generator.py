import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

def generate_password(length, include_letters, include_numbers, include_symbols):
    """Generate a random password based on the user's preferences."""
    character_set = ""
    
    if include_letters:
        character_set += string.ascii_letters
    if include_numbers:
        character_set += string.digits
    if include_symbols:
        character_set += string.punctuation

    if not character_set:
        raise ValueError("No character types selected!")

    password = ''.join(random.choice(character_set) for _ in range(length))
    return password

def generate_and_display_password():
    """Generate password and display it in the GUI."""
    try:
        length = int(length_entry.get())
        include_letters = letters_var.get()
        include_numbers = numbers_var.get()
        include_symbols = symbols_var.get()
        
        password = generate_password(length, include_letters, include_numbers, include_symbols)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Error: {ve}")

def copy_to_clipboard():
    """Copy the generated password to the clipboard."""
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI Setup
app = tk.Tk()
app.title("Advanced Password Generator")

# Length Label and Entry
length_label = tk.Label(app, text="Password Length:")
length_label.grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(app)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkbox for Letters
letters_var = tk.BooleanVar(value=True)
letters_checkbox = tk.Checkbutton(app, text="Include Letters", variable=letters_var)
letters_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Checkbox for Numbers
numbers_var = tk.BooleanVar(value=True)
numbers_checkbox = tk.Checkbutton(app, text="Include Numbers", variable=numbers_var)
numbers_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Checkbox for Symbols
symbols_var = tk.BooleanVar(value=True)
symbols_checkbox = tk.Checkbutton(app, text="Include Symbols", variable=symbols_var)
symbols_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Password Entry
password_entry = tk.Entry(app, width=30)
password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Generate Button
generate_button = tk.Button(app, text="Generate Password", command=generate_and_display_password)
generate_button.grid(row=5, column=0, padx=10, pady=10)

# Copy Button
copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=5, column=1, padx=10, pady=10)

# Run the GUI
app.mainloop()
