import os
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("700x600")
        self.root.configure(bg="#ffffff")
        
        # Theme state
        self.dark_mode = False

        # Directory path variable
        self.directory = tk.StringVar()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame = main_frame  # Store for theme updates
        
        # Top Frame for Dark Mode Toggle
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Dark Mode Toggle Button
        self.dark_mode_toggle = ttk.Checkbutton(
            top_frame, text="Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_toggle.pack(side=tk.RIGHT)
        
        # Directory selection
        dir_frame = ttk.LabelFrame(main_frame, text="Select Directory", padding="10")
        dir_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory, width=50)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)
        
        # Sorting options
        sort_frame = ttk.LabelFrame(main_frame, text="Sorting Options", padding="10")
        sort_frame.pack(fill=tk.X, pady=(0, 20))
        
        btn_file_type = ttk.Button(sort_frame, text="Sort by File Type", command=self.sort_by_file_type)
        btn_file_type.pack(fill=tk.X, pady=5)
        
        btn_alphabetical = ttk.Button(sort_frame, text="Sort Alphabetically", command=self.sort_alphabetically)
        btn_alphabetical.pack(fill=tk.X, pady=5)
        
        btn_date_modified = ttk.Button(sort_frame, text="Sort by Date Modified", command=self.sort_by_date_modified)
        btn_date_modified.pack(fill=tk.X, pady=5)
        
        btn_file_size = ttk.Button(sort_frame, text="Sort by File Size", command=self.sort_by_file_size)
        btn_file_size.pack(fill=tk.X, pady=5)
        
        btn_unscramble = ttk.Button(sort_frame, text="Unscramble Files", command=self.unscramble_files)
        btn_unscramble.pack(fill=tk.X, pady=5)
        
        # Status box
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(status_frame, height=15, state='disabled', bg="#f9f9f9", fg="#000000")
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar to the status box
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text['yscrollcommand'] = scrollbar.set
    
    def toggle_dark_mode(self):
        if self.dark_mode_toggle.instate(['selected']):
            self.dark_mode = True
            self.apply_dark_theme()
        else:
            self.dark_mode = False
            self.apply_light_theme()

    def apply_dark_theme(self):
        dark_bg = "#2e2e2e"
        dark_fg = "#ffffff"
        dark_entry_bg = "#4d4d4d"
        dark_text_bg = "#3c3c3c"
        
        self.root.configure(bg=dark_bg)
        self.main_frame.configure(style='Dark.TFrame')

        # Update all LabelFrames
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.configure(style='Dark.TLabelframe')

        # Update Entry
        self.dir_entry.configure(background=dark_entry_bg, foreground=dark_fg)
        
        # Update Text Widget
        self.status_text.configure(bg=dark_text_bg, fg=dark_fg)
        
        # Update Buttons
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dark.TButton', background=dark_bg, foreground=dark_fg, bordercolor=dark_bg)
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) or isinstance(child, ttk.Checkbutton):
                        child.configure(style='Dark.TButton')

    def apply_light_theme(self):
        light_bg = "#ffffff"
        light_fg = "#000000"
        light_entry_bg = "#ffffff"
        light_text_bg = "#f9f9f9"
        
        self.root.configure(bg=light_bg)
        self.main_frame.configure(style='TFrame')

        # Update all LabelFrames
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.configure(style='TLabelframe')

        # Update Entry
        self.dir_entry.configure(background=light_entry_bg, foreground=light_fg)
        
        # Update Text Widget
        self.status_text.configure(bg=light_text_bg, fg=light_fg)
        
        # Update Buttons
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TButton', background=light_bg, foreground=light_fg, bordercolor=light_bg)
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) or isinstance(child, ttk.Checkbutton):
                        child.configure(style='TButton')

    def browse_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.directory.set(selected_dir)
            self.log_status(f"Selected directory: {selected_dir}")
    
    def log_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
    
    def sort_by_file_type(self):
        directory = self.directory.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        try:
            # Dictionary to map file extensions to folder names
            extension_map = {
                # Images
                '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
                # Documents
                '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents', '.txt': 'Documents',
                # Audio
                '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
                # Video
                '.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video',
                # Archives
                '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
                # Others will go to Misc folder
            }
    
            dir_path = Path(directory)
    
            # Create folders if they don't exist
            for folder in set(extension_map.values()):
                new_dir = dir_path / folder
                new_dir.mkdir(exist_ok=True)
    
            # Create Misc folder for unknown file types
            misc_dir = dir_path / 'Misc'
            misc_dir.mkdir(exist_ok=True)
    
            # Iterate through all files in the directory
            for item in dir_path.iterdir():
                if item.is_file():
                    # Get the file extension
                    file_extension = item.suffix.lower()
                    
                    # Determine destination folder
                    if file_extension in extension_map:
                        dest_folder = dir_path / extension_map[file_extension]
                    else:
                        dest_folder = misc_dir
    
                    # Move the file
                    try:
                        shutil.move(str(item), str(dest_folder / item.name))
                        self.log_status(f"Moved {item.name} to {dest_folder.name}")
                    except Exception as e:
                        self.log_status(f"Error moving {item.name}: {e}")
            self.log_status("Sorting by File Type complete!")
            messagebox.showinfo("Success", "Sorting by File Type complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def sort_alphabetically(self):
        directory = self.directory.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        try:
            dir_path = Path(directory)
    
            # Iterate through all files in the directory
            for item in dir_path.iterdir():
                if item.is_file():
                    # Get the first character of the file name
                    first_char = item.stem[0].upper() if item.stem else 'Others'
                    
                    if first_char.isalpha():
                        # Create folder based on first character
                        dest_folder = dir_path / first_char
                    elif first_char.isdigit():
                        # Files starting with numbers go to '0-9' folder
                        dest_folder = dir_path / '0-9'
                    else:
                        # Non-alphanumeric characters go to 'Others'
                        dest_folder = dir_path / 'Others'
                    
                    dest_folder.mkdir(exist_ok=True)
    
                    # Move the file
                    try:
                        shutil.move(str(item), str(dest_folder / item.name))
                        self.log_status(f"Moved {item.name} to {dest_folder.name}")
                    except Exception as e:
                        self.log_status(f"Error moving {item.name}: {e}")
    
            # After moving all files, sort files within '0-9' folder in ascending order
            numeric_folder = dir_path / '0-9'
            if numeric_folder.exists() and numeric_folder.is_dir():
                # List all files in '0-9' folder
                files = list(numeric_folder.iterdir())
                # Sort files based on numerical prefix
                sorted_files = sorted(
                    files,
                    key=lambda x: self.extract_leading_number(x.stem)
                )
                # Note: Filesystem does not maintain order
                self.log_status("\nFiles in '0-9' folder sorted in ascending order based on leading numbers:")
                for file in sorted_files:
                    self.log_status(f"- {file.name}")
            self.log_status("Sorting Alphabetically complete!")
            messagebox.showinfo("Success", "Sorting Alphabetically complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def extract_leading_number(self, filename):
        number = ''
        for char in filename:
            if char.isdigit():
                number += char
            else:
                break
        return int(number) if number else 0
    
    def sort_by_date_modified(self):
        directory = self.directory.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        try:
            dir_path = Path(directory)
    
            # Iterate through all files in the directory
            for item in dir_path.iterdir():
                if item.is_file():
                    # Get the last modified time
                    modified_time = datetime.fromtimestamp(item.stat().st_mtime)
                    year = modified_time.strftime("%Y")
                    month = modified_time.strftime("%m - %B")
    
                    # Create folder structure Year/Month
                    year_folder = dir_path / year
                    month_folder = year_folder / month
                    month_folder.mkdir(parents=True, exist_ok=True)
    
                    # Move the file
                    try:
                        shutil.move(str(item), str(month_folder / item.name))
                        self.log_status(f"Moved {item.name} to {year}/{month}")
                    except Exception as e:
                        self.log_status(f"Error moving {item.name}: {e}")
            self.log_status("Sorting by Date Modified complete!")
            messagebox.showinfo("Success", "Sorting by Date Modified complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def sort_by_file_size(self):
        directory = self.directory.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        try:
            dir_path = Path(directory)
    
            # Define size categories
            size_categories = {
                'Small (<1MB)': lambda s: s < 1 * 1024 * 1024,
                'Medium (1MB - 100MB)': lambda s: 1 * 1024 * 1024 <= s < 100 * 1024 * 1024,
                'Large (>100MB)': lambda s: s >= 100 * 1024 * 1024
            }
    
            # Iterate through all files in the directory
            for item in dir_path.iterdir():
                if item.is_file():
                    file_size = item.stat().st_size
                    # Determine the size category
                    for category, condition in size_categories.items():
                        if condition(file_size):
                            dest_folder = dir_path / category
                            dest_folder.mkdir(exist_ok=True)
                            break
    
                    # Move the file
                    try:
                        shutil.move(str(item), str(dest_folder / item.name))
                        self.log_status(f"Moved {item.name} to {dest_folder.name}")
                    except Exception as e:
                        self.log_status(f"Error moving {item.name}: {e}")
            self.log_status("Sorting by File Size complete!")
            messagebox.showinfo("Success", "Sorting by File Size complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def unscramble_files(self):
        directory = self.directory.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        try:
            dir_path = Path(directory)
            main_directory = dir_path.resolve()
    
            # Iterate through all subdirectories recursively
            for root, dirs, files in os.walk(directory, topdown=False):
                current_dir = Path(root)
                # Skip the main directory
                if current_dir == main_directory:
                    continue
                for file in files:
                    file_path = current_dir / file
                    dest = main_directory / file_path.name
                    # Handle naming conflicts
                    if dest.exists():
                        base = dest.stem
                        suffix = dest.suffix
                        counter = 1
                        while True:
                            new_name = f"{base}_{counter}{suffix}"
                            new_dest = main_directory / new_name
                            if not new_dest.exists():
                                dest = new_dest
                                break
                            counter += 1
                    try:
                        shutil.move(str(file_path), str(dest))
                        self.log_status(f"Moved {file_path.name} back to {main_directory}")
                    except Exception as e:
                        self.log_status(f"Error moving {file_path.name}: {e}")
                # After moving all files, remove the folder if it's empty
                try:
                    current_dir.rmdir()
                    self.log_status(f"Removed folder: {current_dir.relative_to(main_directory)}")
                except OSError:
                    # Folder not empty (might contain other subdirectories)
                    pass
            self.log_status("Unscrambling complete!")
            messagebox.showinfo("Success", "Unscrambling complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()