import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

DEFAULT_EXTS = [".py", ".js", ".ts", ".java", ".cpp"]

class File2TXTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File2TXT")
        self.geometry("800x600")

        # dark theme colors similar to VS Code
        self.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#d4d4d4")
        style.configure(
            "TButton", background="#3c3c3c", foreground="#d4d4d4", borderwidth=1
        )
        style.map("TButton", background=[("active", "#5a5a5a")])
        style.configure(
            "TEntry",
            fieldbackground="#252526",
            foreground="#d4d4d4",
            insertcolor="#d4d4d4",
        )

        self.folder_var = tk.StringVar()
        self.ext_var = tk.StringVar(value=','.join(e.strip('.') for e in DEFAULT_EXTS))

        folder_frame = ttk.Frame(self)
        folder_frame.pack(padx=10, pady=10, fill=tk.X)
        ttk.Button(folder_frame, text="選擇資料夾", command=self.select_folder).pack(side=tk.LEFT)
        ttk.Label(folder_frame, textvariable=self.folder_var, wraplength=500).pack(side=tk.LEFT, padx=10)

        ext_frame = ttk.Frame(self)
        ext_frame.pack(padx=10, fill=tk.X)
        ttk.Label(ext_frame, text="副檔名(逗號分隔):").pack(side=tk.LEFT)
        ttk.Entry(ext_frame, textvariable=self.ext_var, width=30).pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="開始掃描", command=self.scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="複製全部", command=self.copy_all).pack(side=tk.LEFT, padx=5)

        self.text = scrolledtext.ScrolledText(
            self,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            highlightbackground="#3c3c3c",
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def scan(self):
        folder = self.folder_var.get()
        if not folder:
            messagebox.showwarning("提示", "請先選擇資料夾")
            return

        exts = []
        for ext in self.ext_var.get().split(','):
            ext = ext.strip()
            if not ext:
                continue
            if not ext.startswith('.'):
                ext = '.' + ext
            exts.append(ext)

        results = []
        for root, _, files in os.walk(folder):
            for name in sorted(files):
                if any(name.endswith(e) for e in exts):
                    path = os.path.join(root, name)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    except Exception as exc:
                        content = f"<無法讀取: {exc}>"
                    rel_path = os.path.relpath(path, folder)
                    header = f"\n### {rel_path}\n"
                    results.append(header + content)

        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, '\n'.join(results))

    def copy_all(self):
        """Copy all text in the result box to clipboard."""
        data = self.text.get('1.0', tk.END)
        if not data.strip():
            return
        self.clipboard_clear()
        self.clipboard_append(data)
        messagebox.showinfo("提示", "已複製到剪貼簿")

if __name__ == '__main__':
    app = File2TXTApp()
    app.mainloop()
