import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from yt_dlp import YoutubeDL

def download_video():
    url = url_entry.get()
    download_path = path_var.get()
    filename = filename_entry.get()

    if not url.strip():
        messagebox.showerror("🚨 Error", "Please enter a valid URL.")
        return

    if not download_path.strip():
        messagebox.showerror("🚨 Error", "Please select a download folder.")
        return

    if not filename.strip():
        messagebox.showerror("🚨 Error", "Please enter a filename.")
        return

    try:
        progress_label.config(text="🔄 Preparing to download...")
        progress_bar.start()
        download_button.config(bg="yellow")  # Change button color to yellow during download
        
        options = {
            'format': 'bestvideo',  # Download only the best video
            'outtmpl': os.path.join(download_path, f'{filename}.%(ext)s'),
            'progress_hooks': [lambda d: progress_hook(d)],  # Hook for progress updates
        }

        with YoutubeDL(options) as ydl:
            ydl.download([url])

        download_button.config(bg="green")  # Change button color to green after download
        progress_bar.stop()
        progress_label.config(text="✅ Download completed successfully!")
        messagebox.showinfo("🎉 Success", "Video downloaded successfully!")
        check_disk_space()  # Check disk space after download
    except Exception as e:
        download_button.config(bg="white")  # Reset button color on error
        progress_bar.stop()
        progress_label.config(text="❌ Download failed.")
        messagebox.showerror("🚨 Error", f"An error occurred:\n{str(e)}")

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent = (downloaded / total) * 100
        progress_bar['value'] = percent
        progress_label.config(text=f"📥 Downloading: {percent:.2f}% ({downloaded / (1024**2):.2f} MB of {total / (1024**2):.2f} MB)")

        # Update video size in GUI
        video_size_label.config(text=f"📏 Video Size: {total / (1024**2):.2f} MB")

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)
        download_button.config(state=tk.NORMAL)  # Enable download button
        progress_label.config(text="✅ Download folder selected.")
        check_disk_space()  # Check disk space when folder is selected

def check_disk_space():
    if path_var.get():
        total, used, free = shutil.disk_usage(path_var.get())
        free_space_label.config(text=f"💾 Available Space: {free / (1024**3):.2f} GB")

# Create the main window
root = tk.Tk()
root.title("🎥 YouTube Video Downloader")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# Title label
title_label = tk.Label(root, text="YouTube Video Downloader", bg='#f0f0f0', font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# URL input
tk.Label(root, text="YouTube URL:", bg='#f0f0f0', font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

# Filename input
tk.Label(root, text="File Name (without extension):", bg='#f0f0f0', font=("Arial", 12)).pack(pady=5)
filename_entry = tk.Entry(root, width=50, font=("Arial", 12))
filename_entry.pack(pady=5)

# Folder selection
tk.Label(root, text="Download Folder:", bg='#f0f0f0', font=("Arial", 12)).pack(pady=5)
path_var = tk.StringVar()
path_entry = tk.Entry(root, textvariable=path_var, width=50, font=("Arial", 12))
path_entry.pack(pady=5)
tk.Button(root, text="Browse 📂", command=select_folder, bg='#4CAF50', fg='white', font=("Arial", 10)).pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)
progress_label = tk.Label(root, text="🔍 Select a folder to enable download.", bg='#f0f0f0', font=("Arial", 10))
progress_label.pack()

# Video size label
video_size_label = tk.Label(root, text="📏 Video Size: 0 MB", bg='#f0f0f0', font=("Arial", 10))
video_size_label.pack(pady=5)

# Available space label
free_space_label = tk.Label(root, text="💾 Available Space: 0 GB", bg='#f0f0f0', font=("Arial", 10))
free_space_label.pack(pady=5)

# Download button (initially white)
download_button = tk.Button(root, text="Download 🎬", command=download_video, bg="white", fg="black", font=("Arial", 12), state=tk.DISABLED)
download_button.pack(pady=20)

# Run the GUI loop
root.mainloop()
