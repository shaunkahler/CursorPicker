import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import subprocess
import sys
import logging

# ── logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.expanduser("~"), ".cursor_picker.log")),
        logging.StreamHandler()
    ]
)

# ── persistence ────────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.expanduser("~"), ".cursor_picker_projects.json")

def load_projects():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_projects(projects):
    with open(DATA_FILE, "w") as f:
        json.dump(projects, f, indent=2)

# ── open in cursor ──────────────────────────────────────────────────────────────
def open_in_cursor(path, on_open=None):
    if not os.path.isdir(path):
        logging.error(f"Folder not found: {path}")
        messagebox.showerror("Missing folder", f"Folder no longer exists:\n{path}")
        return
    try:
        logging.info(f"Opening project: {path}")
        if on_open:
            on_open()
        if sys.platform == "win32":
            subprocess.Popen(["cursor", path], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Cursor", path])
        else:
            subprocess.Popen(["cursor", path])
    except Exception as e:
        logging.error(f"Failed to open Cursor: {str(e)}")
        messagebox.showerror("Could not open Cursor", str(e))

# ── UI ─────────────────────────────────────────────────────────────────────────
BG        = "#000000"
CARD_BG   = "#000000"
CARD_HOV  = "#1a1a1a"
ACCENT    = "#ffffff"
ACCENT2   = "#ffffff"
TEXT      = "#ffffff"
SUBTEXT   = "#808080"
BORDER    = "#333333"
DANGER    = "#ff4444"
LOGO      = "#00d4ff"

FONT      = "Segoe UI"

class CursorPicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CursorPicker")
        self.geometry("560x620")
        self.minsize(480, 400)
        self.configure(bg=BG)
        self.projects = load_projects()
        self._status_timer = None
        self._build_ui()
        self._render_projects()

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # header
        hdr = tk.Frame(self, bg=BG, pady=20)
        hdr.pack(fill="x", padx=24)

        tk.Label(hdr, text="⬡  CursorPicker", font=(FONT, 14, "bold"),
                 fg=LOGO, bg=BG).pack(side="left")

        add_btn = tk.Button(
            hdr, text="＋  Add Project",
            font=(FONT, 9, "bold"),
            fg="black", bg=ACCENT,
            activeforeground="black", activebackground=ACCENT2,
            relief="flat", padx=14, pady=7, cursor="hand2",
            command=self._add_project
        )
        add_btn.pack(side="right")
        self._hover(add_btn, ACCENT, ACCENT2)

        # divider
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24)

        # scroll canvas
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=16, pady=12)

        self.canvas = tk.Canvas(outer, bg=BG, bd=0, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview,
                          bg=BG, troughcolor=BG, relief="flat", width=6)
        self.canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.list_frame, anchor="nw"
        )

        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # empty-state label
        self.empty_label = tk.Label(
            self.list_frame,
            text="No projects yet.\nClick  ＋ Add Project  to get started.",
            font=(FONT, 10), fg=SUBTEXT, bg=BG,
            justify="center"
        )

    # ── project cards ─────────────────────────────────────────────────────────
    def _render_projects(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.projects:
            self.empty_label = tk.Label(
                self.list_frame,
                text="No projects yet.\nClick  ＋ Add Project  to get started.",
                font=("Segoe UI", 11), fg=SUBTEXT, bg=BG,
                justify="center", pady=60
            )
            self.empty_label.pack()
            return

        for idx, proj in enumerate(self.projects):
            self._make_card(idx, proj)

        # status label container (inside scroll area)
        status_container = tk.Frame(self.list_frame, bg=BG)
        status_container.pack(fill="x", padx=8, pady=(12, 0))
        self.status_label = tk.Label(
            status_container,
            text="",
            font=(FONT, 12, "bold"), fg=LOGO, bg=BG
        )
        self.status_label.pack(pady=8)

    def _make_card(self, idx, path):
        name = os.path.basename(path) or path

        card = tk.Frame(self.list_frame, bg=CARD_BG, pady=0,
                        highlightbackground=BORDER, highlightthickness=1,
                        cursor="hand2")
        card.pack(fill="x", padx=8, pady=5)

        inner = tk.Frame(card, bg=CARD_BG, padx=16, pady=14)
        inner.pack(fill="both", expand=True)

        # icon + text block
        left = tk.Frame(inner, bg=CARD_BG)
        left.pack(side="left", fill="both", expand=True)

        name_label = tk.Label(left, text="📁  " + name,
                              font=(FONT, 11, "bold"),
                              fg=TEXT, bg=CARD_BG, anchor="w")
        name_label.pack(anchor="w")
        path_label = tk.Label(left, text=path,
                              font=(FONT, 8),
                              fg=SUBTEXT, bg=CARD_BG, anchor="w")
        path_label.pack(anchor="w", pady=(2,0))

        # remove button
        rem = tk.Button(
            inner, text="✕",
            font=(FONT, 10, "bold"), fg=SUBTEXT, bg=CARD_BG,
            activeforeground=DANGER, activebackground=CARD_BG,
            relief="flat", padx=6, pady=0, cursor="hand2",
            command=lambda i=idx: self._remove_project(i)
        )
        rem.pack(side="right", anchor="n")

        # click anywhere on card → open (except the remove button)
        def open_if_not_remove(event, p=path):
            if event.widget != rem:
                self._handle_open(p)

        for widget in (card, inner, left, name_label, path_label):
            widget.bind("<Button-1>", open_if_not_remove)
            widget.bind("<Enter>", lambda e, c=card: c.configure(bg=CARD_HOV))
            widget.bind("<Leave>", lambda e, c=card: c.configure(bg=CARD_BG))

        # child widgets click (but don't rebind hover)
        for widget in inner.winfo_children():
            if widget != rem:
                widget.bind("<Button-1>", open_if_not_remove)

    # ── actions ───────────────────────────────────────────────────────────────
    def _handle_open(self, path):
        logging.info(f"User clicked to open: {path}")
        self.status_label.configure(text="opening file...")
        if self._status_timer:
            self.after_cancel(self._status_timer)
        try:
            open_in_cursor(path)
        finally:
            self._status_timer = self.after(1500, lambda: self.status_label.configure(text=""))

    def _add_project(self):
        folder = filedialog.askdirectory(title="Select project folder")
        if not folder:
            return
        if folder in self.projects:
            messagebox.showinfo("Already added", "That folder is already in your list.")
            return
        self.projects.append(folder)
        save_projects(self.projects)
        self._render_projects()

    def _remove_project(self, idx):
        name = os.path.basename(self.projects[idx])
        if messagebox.askyesno("Remove project", f'Remove "{name}" from the list?\n(The folder itself won\'t be deleted.)'):
            self.projects.pop(idx)
            save_projects(self.projects)
            self._render_projects()

    # ── scroll helpers ────────────────────────────────────────────────────────
    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── generic hover ─────────────────────────────────────────────────────────
    def _hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal))


if __name__ == "__main__":
    app = CursorPicker()
    app.mainloop()
