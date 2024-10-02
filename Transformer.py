import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, filedialog, ttk
from PIL import Image
import pillow_heif
import os
import subprocess

# Global variable for the output directory
output_directory = os.path.join(os.path.expanduser("~"), "Downloads")


# Function to convert HEIC files to JPG with progress bar updates
def convert_to_jpg(file_paths):
    total_files = len(file_paths)
    for i, file in enumerate(file_paths):
        try:
            # Open HEIC file using pillow_heif
            heif_file = pillow_heif.open_heif(file)
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)

            # Convert HEIC to JPG and save to the selected output folder
            output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(file))[0] + ".jpg")
            image.save(output_file, "JPEG")
            #print(f"Converted: {file} -> {output_file}")
        except Exception as e:
            #print(f"Failed to convert {file}: {e}")
            messagebox.showerror("Error", f"Failed to convert {file}: {e}")

        # Update the progress bar
        progress_var.set((i + 1) / total_files * 100)
        progress_bar.update()

    messagebox.showinfo("Success", f"All files have been successfully converted and saved to {output_directory}!")
    # Automatically open the output directory
    open_output_directory()


# Function to handle file drop
def on_drop(event):
    file_paths = root.tk.splitlist(event.data)
    for file in file_paths:
        if file.lower().endswith('.heic'):
            files_listbox.insert(tk.END, file)
        else:
            messagebox.showwarning("Warning", f"{file} is not a HEIC file.")

    if files_listbox.size() > 0:
        convert_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)


# Function to clear the listbox
def clear_listbox():
    files_listbox.delete(0, tk.END)
    convert_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)


# Function to start conversion when button is clicked
def start_conversion():
    file_paths = files_listbox.get(0, tk.END)
    if file_paths:
        progress_var.set(0)
        convert_to_jpg(file_paths)


# Function to choose a custom output directory
def choose_output_directory():
    global output_directory
    directory = filedialog.askdirectory()
    if directory:
        output_directory = directory
    else:
        output_directory = os.path.join(os.path.expanduser("~"), "Downloads")
    directory_label.config(text=f"Output Directory: {output_directory}")


# Function to open the output directory automatically after conversion
def open_output_directory():
    if os.name == "nt":  # Windows
        subprocess.Popen(f'explorer "{output_directory}"')
    elif os.name == "posix":  # macOS or Linux
        subprocess.Popen(["open", output_directory])


# GUI setup
root = TkinterDnD.Tk()  # Use TkinterDnD.Tk() instead of tk.Tk() for drag-and-drop support
root.title("HEIC to JPG Converter")
root.geometry("600x350")

# Instruction label
label = tk.Label(root, text="Drag and drop your HEIC files here:", font=("Arial", 12))
label.pack(pady=10)

# Listbox to display dragged files
files_listbox = tk.Listbox(root, width=80, height=5)
files_listbox.pack(pady=10)

# Frame to hold the buttons side by side
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Button to convert files, placed in the button frame
convert_button = tk.Button(button_frame, text="Convert to JPG", state=tk.DISABLED, command=start_conversion)
convert_button.pack(side=tk.LEFT, padx=5)

# Button to clear files, placed next to the convert button in the button frame
clear_button = tk.Button(button_frame, text="Clear Files", state=tk.DISABLED, command=clear_listbox)
clear_button.pack(side=tk.LEFT, padx=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=20)

# Label to display output directory
directory_label = tk.Label(root, text=f"Output Directory: {output_directory}", font=("Arial", 10))
directory_label.pack(pady=10)

# Add drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Run the application
root.mainloop()
