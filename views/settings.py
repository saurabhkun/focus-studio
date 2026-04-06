import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from styles import theme

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
DEFAULT_SETTINGS = {
    "work_duration": 25,
    "short_break": 5,
    "long_break": 15,
    "sessions_before_long": 4,
    "monthly_goal_hours": 20,
    "music_folder": "",
    "last_username": ""
}

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_PATH, "r") as f:
            data = json.load(f)
            # Merge with defaults
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(data):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

class SettingsScreen(tk.Frame):
    def __init__(self, parent, user_data, logout_callback):
        super().__init__(parent, bg=theme.BG_MAIN)
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.settings = load_settings()
        
        self.setup_ui()

    def setup_ui(self):
        lbl_title = tk.Label(self, text="Settings", font=theme.FONT_TITLE, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY)
        lbl_title.pack(pady=20, anchor="w", padx=40)
        
        card = tk.Frame(self, bg=theme.BG_CARD, padx=30, pady=30)
        card.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Grid formulation
        fields = [
            ("Work Duration (min):", "work_duration"),
            ("Short Break (min):", "short_break"),
            ("Long Break (min):", "long_break"),
            ("Sessions before Long Break:", "sessions_before_long"),
            ("Monthly Goal (hours):", "monthly_goal_hours")
        ]
        
        self.entries = {}
        for i, (label_text, key) in enumerate(fields):
            lbl = tk.Label(card, text=label_text, font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY)
            lbl.grid(row=i, column=0, sticky="w", pady=10)
            
            ent = tk.Entry(card, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY)
            ent.insert(0, str(self.settings.get(key, "")))
            ent.grid(row=i, column=1, sticky="w", pady=10, padx=20)
            self.entries[key] = ent
            
        # Music folder
        lbl_music = tk.Label(card, text="Music Folder:", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY)
        lbl_music.grid(row=len(fields), column=0, sticky="w", pady=10)
        
        music_frame = tk.Frame(card, bg=theme.BG_CARD)
        music_frame.grid(row=len(fields), column=1, sticky="w", pady=10, padx=20)
        
        self.music_path_var = tk.StringVar(value=self.settings.get("music_folder", ""))
        ent_music = tk.Entry(music_frame, textvariable=self.music_path_var, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY, width=30)
        ent_music.pack(side="left")
        
        btn_browse = tk.Button(music_frame, text="Browse", font=theme.FONT_SMALL, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat", command=self.browse_music)
        btn_browse.pack(side="left", padx=5)
        
        # Save Button
        btn_save = tk.Button(card, text="Save Settings", font=theme.FONT_BTN, bg=theme.SUCCESS, fg=theme.TEXT_PRIMARY, relief="flat", command=self.save_all, padx=20, pady=10)
        btn_save.grid(row=len(fields)+1, column=0, columnspan=2, pady=30)
        
        # Logout
        btn_logout = tk.Button(card, text="Log Out", font=theme.FONT_BTN, bg=theme.DANGER, fg=theme.TEXT_PRIMARY, relief="flat", command=self.logout_callback, padx=20, pady=10)
        btn_logout.grid(row=len(fields)+2, column=0, columnspan=2, pady=10)

    def browse_music(self):
        folder = filedialog.askdirectory()
        if folder:
            self.music_path_var.set(folder)

    def save_all(self):
        try:
            self.settings["work_duration"] = int(self.entries["work_duration"].get())
            self.settings["short_break"] = int(self.entries["short_break"].get())
            self.settings["long_break"] = int(self.entries["long_break"].get())
            self.settings["sessions_before_long"] = int(self.entries["sessions_before_long"].get())
            self.settings["monthly_goal_hours"] = int(self.entries["monthly_goal_hours"].get())
            self.settings["music_folder"] = self.music_path_var.get()
            
            save_settings(self.settings)
            messagebox.showinfo("Success", "Settings saved successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for durations.")
