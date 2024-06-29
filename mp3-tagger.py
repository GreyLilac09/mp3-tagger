import tkinter as tk
from tkinter import ttk, filedialog
import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB
import re

class MP3TagEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Tag Editor")

        # Calculate window size (80% of screen width, 80% of screen height)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}")
        self.root.resizable(True, True)

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create two columns
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # First column: File browser
        self.create_file_browser()

        # Second column: Tag viewer and editor
        self.create_tag_viewer_editor()

    def create_file_browser(self):
        file_frame = ttk.Frame(self.main_frame)
        file_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # Create Treeview
        self.tree = ttk.Treeview(file_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

        # Configure Treeview
        self.tree.heading('#0', text='Folders and MP3 Files', anchor=tk.W)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Browse button
        browse_button = ttk.Button(self.main_frame, text="Browse Root Folder", command=self.browse_directory)
        browse_button.grid(row=1, column=0, pady=(0, 10))

    def create_tag_viewer_editor(self):
        editor_frame = ttk.Frame(self.main_frame)
        editor_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(5, 10), pady=10)

        # Selected file name
        file_label_frame = ttk.Frame(editor_frame)
        file_label_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(file_label_frame, text="Selected file:", font=("", 12, "bold")).pack(side=tk.LEFT)
        self.selected_file_label = tk.Entry(file_label_frame, font=("", 12), state="readonly", readonlybackground="white", relief="flat")
        self.selected_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # File rename frame
        rename_frame = ttk.Frame(editor_frame)
        rename_frame.pack(fill=tk.X, padx=5, pady=(0, 10))

        ttk.Label(rename_frame, text="New file name:").pack(side=tk.LEFT)
        self.new_filename_entry = ttk.Entry(rename_frame, width=40)
        self.new_filename_entry.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(rename_frame, text="Rename", command=self.rename_file).pack(side=tk.LEFT)

        # Tags frame
        tags_frame = ttk.LabelFrame(editor_frame, text="Edit Tags")
        tags_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header row
        ttk.Label(tags_frame, text="Current Tags", font=("", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(tags_frame, text="New Tags", font=("", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        # Title
        ttk.Label(tags_frame, text="Title:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.current_title = tk.Entry(tags_frame, width=30, state="readonly", readonlybackground="white")
        self.current_title.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(tags_frame, width=30)
        self.title_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Artist
        ttk.Label(tags_frame, text="Artist:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.current_artist = tk.Entry(tags_frame, width=30, state="readonly", readonlybackground="white")
        self.current_artist.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.artist_entry = ttk.Entry(tags_frame, width=30)
        self.artist_entry.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Album
        ttk.Label(tags_frame, text="Album:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.current_album = tk.Entry(tags_frame, width=30, state="readonly", readonlybackground="white")
        self.current_album.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.album_entry = ttk.Entry(tags_frame, width=30)
        self.album_entry.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Button frame
        button_frame = ttk.Frame(tags_frame)
        button_frame.grid(row=4, column=1, columnspan=2, pady=10)

        # Auto-parse button
        auto_parse_button = ttk.Button(button_frame, text="Auto-Parse", command=self.auto_parse_filename)
        auto_parse_button.pack(side=tk.LEFT, padx=(0, 10))

        # Update button
        update_button = ttk.Button(button_frame, text="Update Tags", command=self.update_tags)
        update_button.pack(side=tk.LEFT)

        self.status_label = ttk.Label(editor_frame, text="")
        self.status_label.pack(pady=5)

    def auto_parse_filename(self):
        selected_items = self.tree.selection()
        if not selected_items:
            self.status_label.config(text="Please select an MP3 file first.", foreground="red")
            return

        file_path = self.tree.item(selected_items[0])['values'][0]
        if not file_path.lower().endswith('.mp3'):
            self.status_label.config(text="Please select an MP3 file.", foreground="red")
            return

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Try to parse artist and title
        match = re.match(r'^(.*?)\s*-\s*(.*?)(?:\s*\[.*?\])?$', file_name)
        if match:
            artist, title = match.groups()
            self.artist_entry.delete(0, tk.END)
            self.artist_entry.insert(0, artist.strip())
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title.strip())
            self.status_label.config(text="Auto-parse successful", foreground="green")
        else:
            self.status_label.config(text="Couldn't parse artist and title from filename", foreground="orange")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.tree.delete(*self.tree.get_children())
            self.populate_tree(directory)

    def populate_tree(self, path, parent=''):
        folder_icon = self.tree.insert(parent, 'end', text=os.path.basename(path), open=False, values=[path])
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self.populate_tree(item_path, folder_icon)
            elif item.lower().endswith('.mp3'):
                self.tree.insert(folder_icon, 'end', text=item, values=[item_path])

    def on_select(self, event):
        selected_item = self.tree.selection()[0]
        file_path = self.tree.item(selected_item)['values'][0]
        if file_path.lower().endswith('.mp3'):
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            self.selected_file_label.config(state="normal")
            self.selected_file_label.delete(0, tk.END)
            self.selected_file_label.insert(0, file_name_without_ext)
            self.selected_file_label.config(state="readonly")
            self.new_filename_entry.delete(0, tk.END)
            self.new_filename_entry.insert(0, file_name_without_ext)
            self.load_tags(file_path)
        else:
            self.clear_tags()

    def load_tags(self, file_path):
        try:
            audio = ID3(file_path)
            title = str(audio.get('TIT2', [''])[0])
            artist = str(audio.get('TPE1', [''])[0])
            album = str(audio.get('TALB', [''])[0])

            # Update current tags display
            self.current_title.config(state="normal")
            self.current_title.delete(0, tk.END)
            self.current_title.insert(0, title)
            self.current_title.config(state="readonly")

            self.current_artist.config(state="normal")
            self.current_artist.delete(0, tk.END)
            self.current_artist.insert(0, artist)
            self.current_artist.config(state="readonly")

            self.current_album.config(state="normal")
            self.current_album.delete(0, tk.END)
            self.current_album.insert(0, album)
            self.current_album.config(state="readonly")

            # Populate edit fields
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.artist_entry.delete(0, tk.END)
            self.artist_entry.insert(0, artist)
            self.album_entry.delete(0, tk.END)
            self.album_entry.insert(0, album)

            self.status_label.config(text="Tags loaded successfully", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Error loading tags: {str(e)}", foreground="red")

    def clear_tags(self):
        for widget in (self.current_title, self.current_artist, self.current_album,
                       self.title_entry, self.artist_entry, self.album_entry):
            widget.delete(0, tk.END)
        self.selected_file_label.config(state="normal")
        self.selected_file_label.delete(0, tk.END)
        self.selected_file_label.config(state="readonly")
        self.status_label.config(text="")

    def update_tags(self):
        selected_items = self.tree.selection()
        if not selected_items:
            self.status_label.config(text="Please select an MP3 file first.", foreground="red")
            return

        file_path = self.tree.item(selected_items[0])['values'][0]
        if not file_path.lower().endswith('.mp3'):
            self.status_label.config(text="Please select an MP3 file.", foreground="red")
            return

        try:
            audio = ID3(file_path)
            audio['TIT2'] = TIT2(encoding=3, text=self.title_entry.get())
            audio['TPE1'] = TPE1(encoding=3, text=self.artist_entry.get())
            audio['TALB'] = TALB(encoding=3, text=self.album_entry.get())
            audio.save()
            self.status_label.config(text="Tags updated successfully!", foreground="green")
            self.load_tags(file_path)  # Reload tags to update the display
        except Exception as e:
            self.status_label.config(text=f"Error updating tags: {str(e)}", foreground="red")

    def rename_file(self):
        selected_items = self.tree.selection()
        if not selected_items:
            self.status_label.config(text="Please select an MP3 file first.", foreground="red")
            return

        old_path = self.tree.item(selected_items[0])['values'][0]
        if not old_path.lower().endswith('.mp3'):
            self.status_label.config(text="Please select an MP3 file.", foreground="red")
            return

        new_filename = self.new_filename_entry.get().strip()
        if not new_filename:
            self.status_label.config(text="Please enter a new file name.", foreground="red")
            return

        new_filename = f"{new_filename}.mp3"
        new_path = os.path.join(os.path.dirname(old_path), new_filename)

        try:
            os.rename(old_path, new_path)
            self.status_label.config(text="File renamed successfully.", foreground="green")
            
            # Update the tree view
            parent = self.tree.parent(selected_items[0])
            self.tree.delete(selected_items[0])
            self.tree.insert(parent, 'end', text=new_filename, values=[new_path])
            
            # Update the selected file label
            self.selected_file_label.config(state="normal")
            self.selected_file_label.delete(0, tk.END)
            self.selected_file_label.insert(0, os.path.splitext(new_filename)[0])
            self.selected_file_label.config(state="readonly")

            # Reload tags for the renamed file
            self.load_tags(new_path)
        except Exception as e:
            self.status_label.config(text=f"Error renaming file: {str(e)}", foreground="red")

        
if __name__ == "__main__":
    root = tk.Tk()
    app = MP3TagEditor(root)
    root.mainloop()