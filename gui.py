import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from file_sorter import FileSorter


class FileManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📂 Smart File Manager v1.0")
        self.root.geometry("640x520")
        self.root.minsize(520, 420)

        self.folder_var = tk.StringVar()
        self.action_var = tk.StringVar(value="move")
        self.preview_var = tk.StringVar(value="Select a folder to preview files")
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()

    def _build_ui(self):
        padding = {"padx": 12, "pady": 6}

        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill="x", **padding)

        ttk.Label(folder_frame, text="Folder:").pack(side="left")
        ttk.Entry(folder_frame, textvariable=self.folder_var).pack(
            side="left", fill="x", expand=True, padx=(8, 8)
        )
        ttk.Button(folder_frame, text="Browse", command=self._browse).pack(side="left")

        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", **padding)

        ttk.Label(action_frame, text="Action:").pack(side="left")
        ttk.Radiobutton(
            action_frame, text="Move files", variable=self.action_var, value="move"
        ).pack(side="left", padx=(8, 16))
        ttk.Radiobutton(
            action_frame, text="Copy files", variable=self.action_var, value="copy"
        ).pack(side="left")

        preview_frame = ttk.LabelFrame(self.root, text="Preview")
        preview_frame.pack(fill="x", **padding)
        ttk.Label(preview_frame, textvariable=self.preview_var, wraplength=580).pack(
            anchor="w", padx=8, pady=8
        )

        self.sort_btn = ttk.Button(
            self.root,
            text="📂 Sort Files",
            command=self._sort
        )
        self.sort_btn.pack(pady=8)
        
        self.progress = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            length=300
        )
        self.progress.pack(pady=(0, 8))

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=12)
        
        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self._clear_log
        ).pack(side="right")

        log_frame = ttk.LabelFrame(self.root, text="Log")
        log_frame.pack(fill="both", expand=True, **padding)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=14, state="disabled", wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=8)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom", **padding)
        ttk.Label(status_frame, text="Status:").pack(side="left")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left", padx=(8, 0))

    def _browse(self):
        folder = filedialog.askdirectory(title="Select folder to sort")
        if folder:
            self.folder_var.set(folder)
            self._update_preview()

    def _update_preview(self):
        folder = self.folder_var.get().strip()
        if not folder:
            self.preview_var.set("Select a folder to preview files")
            return

        try:
            preview = FileSorter(folder).preview()
        except OSError as exc:
            self.preview_var.set(f"Cannot read folder: {exc}")
            return

        if not preview:
            self.preview_var.set("No files to sort in this folder")
            return

        parts = [f"{category}: {count}" for category, count in sorted(preview.items())]
        self.preview_var.set(" | ".join(parts))
    
    def _append_log(self, text: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _sort(self):
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("No folder", "Please select a folder first.")
            return

        action = self.action_var.get()
        confirm = messagebox.askyesno(
            "Confirm Sorting",
            f"Do you want to {action} all supported files?"
        )

if not confirm:
    return
        self._clear_log()
        self.status_var.set("Sorting...")
        self.root.update_idletasks()
        self.sort_btn.config(state="disabled")i
        self.progress.start(10)

        try:
            result = FileSorter(folder, action=action).sort()
        except OSError as exc:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"Could not access folder:\n{exc}")
            self.progress.stop()
            self.sort_btn.config(state="normal")
            return

        if result["total"] == 0:
            self.status_var.set("Ready")
            messagebox.showinfo("No files", "No files to sort in this folder.")
            self._update_preview()
            self.progress.stop()
            self.sort_btn.config(state="normal")
            return

        for line in result["log"]:
            self._append_log(line)
        for error in result["errors"]:
            self._append_log(f"ERROR: {error}")

        verb = "moved" if action == "move" else "copied"
        self._append_log(f"\nDone — {result['total']} file(s) {verb}.")
        self.status_var.set(f"Done — {result['total']} files organized")
        self.progress.stop()
        self.sort_btn.config(state="normal")
        self._update_preview()

    def run(self):
        self.root.mainloop()
