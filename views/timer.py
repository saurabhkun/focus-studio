import tkinter as tk
from tkinter import ttk
from styles import theme
from logic import utils
from views import settings
from logic import database
import random
from plyer import notification
from datetime import datetime

class TimerScreen(tk.Frame):
    def __init__(self, parent, user_data, bg):
        super().__init__(parent, bg=bg)
        self.user_data = user_data
        self.settings = settings.load_settings()
        
        self.mode = "work"
        self.is_running = False
        self.sessions_completed = 0
        self.time_left = self.settings["work_duration"] * 60
        self.total_time = self.time_left
        
        self.quote_var = tk.StringVar(value=random.choice(utils.MOTIVATIONAL_QUOTES))
        
        self.pulse_dir = 0.5
        self.pulse_width = 15.0

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg=theme.BG_MAIN)
        header_frame.pack(fill="x", pady=20, padx=40)
        
        tk.Label(header_frame, text="Pomodoro Timer", font=theme.FONT_TITLE, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY).pack(side="left")
        
        # Subject Selector
        self.subject_var = tk.StringVar(value="General Study")
        subjects = ["General Study", "Math", "Science", "History", "Programming"]
        sub_dropdown = ttk.Combobox(header_frame, textvariable=self.subject_var, values=subjects, font=theme.FONT_BODY, state="readonly")
        sub_dropdown.pack(side="right")
        
        # Mode buttons
        mode_frame = tk.Frame(self, bg=theme.BG_CARD, padx=10, pady=10)
        mode_frame.pack(pady=10)
        
        self.btn_work = tk.Button(mode_frame, text="Work", font=theme.FONT_BTN, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat", command=lambda: self.switch_mode("work"))
        self.btn_work.pack(side="left", padx=5)
        
        self.btn_short = tk.Button(mode_frame, text="Short Break", font=theme.FONT_BTN, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY, relief="flat", command=lambda: self.switch_mode("short_break"))
        self.btn_short.pack(side="left", padx=5)
        
        self.btn_long = tk.Button(mode_frame, text="Long Break", font=theme.FONT_BTN, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY, relief="flat", command=lambda: self.switch_mode("long_break"))
        self.btn_long.pack(side="left", padx=5)
        
        # Session dots
        self.lbl_dots = tk.Label(self, text="○ ○ ○ ○", font=theme.FONT_HEADING, bg=theme.BG_MAIN, fg=theme.TEXT_SECONDARY)
        self.lbl_dots.pack(pady=5)
        
        # Canvas for ring
        self.canvas_size = 300
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg=theme.BG_MAIN, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Timer text
        self.text_id = self.canvas.create_text(self.canvas_size/2, self.canvas_size/2, text=utils.format_timer_display(self.time_left), font=("Helvetica", 48, "bold"), fill=theme.TEXT_PRIMARY)
        
        # Controls
        ctrl_frame = tk.Frame(self, bg=theme.BG_MAIN)
        ctrl_frame.pack(pady=10)
        
        self.btn_action = tk.Button(ctrl_frame, text="Start", font=theme.FONT_TITLE, bg=theme.SUCCESS, fg=theme.TEXT_PRIMARY, relief="flat", command=self.toggle_timer, padx=40)
        self.btn_action.pack(side="left", padx=10)
        
        btn_reset = tk.Button(ctrl_frame, text="Reset", font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, relief="flat", command=self.reset_timer, padx=20)
        btn_reset.pack(side="left", padx=10)
        
        # Quote
        lbl_quote = tk.Label(self, textvariable=self.quote_var, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_SECONDARY, wraplength=400, justify="center")
        lbl_quote.pack(pady=30)
        
        self.draw_ring()

    def get_color(self):
        if self.mode == "work":
            return theme.ACCENT
        elif self.mode == "short_break":
            return theme.ACCENT2
        else:
            return theme.SUCCESS

    def update_dots(self):
        total_needed = self.settings["sessions_before_long"]
        completed = self.sessions_completed % total_needed
        dots = " ".join(["●" if i < completed else "○" for i in range(total_needed)])
        self.lbl_dots.configure(text=dots)

    def switch_mode(self, mode):
        self.mode = mode
        self.is_running = False
        self.btn_action.configure(text="Start", bg=theme.SUCCESS)
        
        self.btn_work.configure(bg=theme.ACCENT if mode == "work" else theme.BG_CARD, fg=theme.TEXT_PRIMARY if mode == "work" else theme.TEXT_SECONDARY)
        self.btn_short.configure(bg=theme.ACCENT2 if mode == "short_break" else theme.BG_CARD, fg=theme.TEXT_PRIMARY if mode == "short_break" else theme.TEXT_SECONDARY)
        self.btn_long.configure(bg=theme.SUCCESS if mode == "long_break" else theme.BG_CARD, fg=theme.TEXT_PRIMARY if mode == "long_break" else theme.TEXT_SECONDARY)
        
        if mode == "work":
            self.total_time = self.settings["work_duration"] * 60
        elif mode == "short_break":
            self.total_time = self.settings["short_break"] * 60
        else:
            self.total_time = self.settings["long_break"] * 60
            
        self.time_left = self.total_time
        self.update_display()
        self.draw_ring()

    def update_display(self):
        self.canvas.itemconfig(self.text_id, text=utils.format_timer_display(self.time_left))
        
    def draw_ring(self):
        self.canvas.delete("ring")
        self.canvas.delete("bg_ring")
        
        pad = 20
        # Background track
        self.canvas.create_oval(pad, pad, self.canvas_size-pad, self.canvas_size-pad, outline=theme.BG_CARD, width=15, tags="bg_ring")
        
        extent = (self.time_left / max(1, self.total_time)) * 360
        if extent > 0:
            self.ring_id = self.canvas.create_arc(pad, pad, self.canvas_size-pad, self.canvas_size-pad, start=90, extent=extent, style=tk.ARC, outline=self.get_color(), width=self.pulse_width, tags="ring")

    def toggle_timer(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.btn_action.configure(text="Pause", bg=theme.WARNING)
            self.tick()
        else:
            self.btn_action.configure(text="Resume", bg=theme.SUCCESS)

    def reset_timer(self):
        self.is_running = False
        self.btn_action.configure(text="Start", bg=theme.SUCCESS)
        self.time_left = self.total_time
        self.pulse_width = 15.0
        self.update_display()
        self.draw_ring()

    def tick(self):
        if not self.is_running:
            return
            
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            
            # Pulse animation
            self.pulse_width += self.pulse_dir
            if self.pulse_width > 18 or self.pulse_width < 14:
                self.pulse_dir *= -1
                
            self.draw_ring()
            self.after(1000, self.tick)
        else:
            self.complete_session()

    def complete_session(self):
        self.is_running = False
        self.btn_action.configure(text="Start", bg=theme.SUCCESS)
        
        xp_gain = 0
        dur_mins = 0
        if self.mode == "work":
            xp_gain = 25
            dur_mins = self.settings["work_duration"]
            self.sessions_completed += 1
            
            # Auto switch to break
            if self.sessions_completed % self.settings["sessions_before_long"] == 0:
                self.switch_mode("long_break")
            else:
                self.switch_mode("short_break")
        else:
            xp_gain = 5
            # From break to work
            self.switch_mode("work")
            
        self.update_dots()
        self.quote_var.set(random.choice(utils.MOTIVATIONAL_QUOTES))
        
        # Update user session
        today = datetime.now().strftime("%Y-%m-%d")
        database.execute_query("INSERT INTO sessions (user_id, subject, duration_minutes, session_type, date, xp_earned) VALUES (?, ?, ?, ?, ?, ?)", 
                               (self.user_data['id'], self.subject_var.get(), dur_mins, self.mode, today, xp_gain))
                               
        database.update_user_stats(self.user_data['id'], xp_gain, dur_mins)
        
        # Badge logic
        self.check_badges(dur_mins)

        # Notify
        try:
            notification.notify(title="Focus Studio", message="Session complete! Take a break 🎉", app_name="Focus Studio")
        except:
            pass

    def check_badges(self, dur_mins):
        uid = self.user_data['id']
        # check first session
        sess_count = database.fetch_one("SELECT COUNT(*) as c FROM sessions WHERE user_id = ?", (uid,))['c']
        if sess_count == 1:
            database.add_badge(uid, "first_session")
            
        # check night owl / early bird
        hr = datetime.now().hour
        if hr >= 22:
            database.add_badge(uid, "night_owl")
        if hr <= 6:
            database.add_badge(uid, "early_bird")

        # Update streak? simplified if last_study_date != today
        usr = database.get_user_by_id(uid)
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = usr['last_study_date']
        
        if last_date != today:
            # check if last_date was yesterday
            # Simplified streak update
            new_streak = usr['streak'] + 1
            database.execute_query("UPDATE users SET streak = ?, last_study_date = ? WHERE id = ?", (new_streak, today, uid))
            if new_streak >= 3: database.add_badge(uid, "streak_3")
            if new_streak >= 7: database.add_badge(uid, "streak_7")
