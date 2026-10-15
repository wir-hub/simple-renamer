import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD

class SimpleRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Renamer")
        self.root.geometry("500x420")
        self.root.resizable(False, False)

        self.files = []

        # Drag & drop area
        self.drop_label = tk.Label(root, text="Drag files here\nor click to browse", 
                                   bg="#e8f4f8", relief="groove", height=6, font=("Segoe UI", 10))
        self.drop_label.pack(fill="x", padx=20, pady=10)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind("<Button-1>", self.browse_files)

        # File list
        self.listbox = tk.Listbox(root, height=8)
        self.listbox.pack(fill="both", expand=True, padx=20, pady=5)

        # Name input
        name_frame = tk.Frame(root)
        name_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(name_frame, text="New name:").pack(side="left")
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Numbering option
        self.add_number = tk.BooleanVar()
        tk.Checkbutton(root, text="Add number (01, 02, ...)", variable=self.add_number).pack(anchor="w", padx=20)

        # Buttons + made by
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10, fill="x", padx=20)
        tk.Button(btn_frame, text="Rename", command=self.rename_files, bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear, width=12).pack(side="left", padx=5)
        tk.Label(btn_frame, text="wirsoft", fg="#888888", font=("Segoe UI", 8)).pack(side="right", padx=5)

    def on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        for p in paths:
            if os.path.isfile(p):
                self.files.append(p)
        self.update_list()

    def browse_files(self, event=None):
        files = filedialog.askopenfilenames(title="Select files")
        if files:
            self.files.extend(files)
            self.update_list()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for f in self.files:
            self.listbox.insert(tk.END, os.path.basename(f))

    def clear(self):
        self.files = []
        self.listbox.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)

    def rename_files(self):
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Warning", "Please enter a new name.")
            return
        if not self.files:
            messagebox.showwarning("Warning", "No files selected.")
            return

        add_num = self.add_number.get()
        errors = []

        for i, filepath in enumerate(self.files, start=1):
            path = Path(filepath)
            ext = path.suffix
            if add_num:
                final_name = f"{new_name} {i:02d}{ext}"
            else:
                final_name = f"{new_name}{ext}"

            new_path = path.parent / final_name
            try:
                if new_path.exists():
                    errors.append(f"{final_name} already exists")
                    continue
                path.rename(new_path)
            except Exception as e:
                errors.append(f"{path.name}: {str(e)}")

        if errors:
            messagebox.showerror("Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Done", f"Renamed {len(self.files)} files successfully!")
            self.clear()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SimpleRenamer(root)
    root.mainloop()
