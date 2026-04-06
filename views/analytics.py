import tkinter as tk
from datetime import datetime, timedelta
from styles import theme
from logic import database

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsScreen(tk.Frame):
    def __init__(self, parent, user_data, bg):
        super().__init__(parent, bg=bg)
        self.user_data = user_data
        self.bg = bg
        
        self.setup_ui()

    def load_data(self):
        uid = self.user_data['id']
        
        # Last 7 days chart data
        self.days = []
        self.mins_per_day = []
        for i in range(6, -1, -1):
            d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            self.days.append(d[-5:]) # MM-DD
            
            res = database.fetch_one("SELECT SUM(duration_minutes) as sm FROM sessions WHERE user_id=? AND date=?", (uid, d))
            self.mins_per_day.append(res['sm'] if res['sm'] else 0)
            
        # Pie chart data
        self.subjects = []
        self.subject_mins = []
        res = database.fetch_all("SELECT subject, SUM(duration_minutes) as sm FROM sessions WHERE user_id=? GROUP BY subject", (uid,))
        for r in res:
            self.subjects.append(r['subject'])
            self.subject_mins.append(r['sm'])
            
        # Stats
        self.total_sessions = database.fetch_one("SELECT COUNT(*) as c FROM sessions WHERE user_id=?", (uid,))['c'] or 0
        if sum(self.mins_per_day) > 0:
            best_idx = self.mins_per_day.index(max(self.mins_per_day))
            self.best_day = self.days[best_idx]
        else:
            self.best_day = "N/A"
            
        if self.subject_mins:
            best_sub_idx = self.subject_mins.index(max(self.subject_mins))
            self.best_subj = self.subjects[best_sub_idx]
        else:
            self.best_subj = "N/A"
            
        self.avg_len = (sum(self.mins_per_day) // max(1, self.total_sessions)) if self.total_sessions else 0

    def setup_ui(self):
        self.load_data()
        
        lbl_title = tk.Label(self, text="Analytics", font=theme.FONT_TITLE, bg=self.bg, fg=theme.TEXT_PRIMARY)
        lbl_title.pack(anchor="w", padx=40, pady=(20, 10))
        
        # Stats Cards
        stats_frame = tk.Frame(self, bg=self.bg)
        stats_frame.pack(fill="x", padx=40, pady=10)
        
        cards = [
            ("Best Day (Last 7)", self.best_day),
            ("Top Subject", self.best_subj),
            ("Avg Session", f"{self.avg_len}m")
        ]
        
        for lbl, val in cards:
            c = tk.Frame(stats_frame, bg=theme.BG_CARD, padx=20, pady=15, width=200)
            c.pack(side="left", padx=(0, 20))
            c.pack_propagate(False)
            tk.Label(c, text=val, font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.ACCENT).pack()
            tk.Label(c, text=lbl, font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack()
            
        # Charts Area
        charts_frame = tk.Frame(self, bg=self.bg)
        charts_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.plot_bar_chart(charts_frame)
        self.plot_pie_chart(charts_frame)
        self.draw_streak_calendar(charts_frame)

    def plot_bar_chart(self, parent):
        frame = tk.Frame(parent, bg=theme.BG_CARD)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(frame, text="Study Time (Last 7 Days)", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(pady=10)
        
        fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
        fig.patch.set_facecolor(theme.BG_CARD)
        ax.set_facecolor(theme.BG_CARD)
        
        ax.bar(self.days, self.mins_per_day, color=theme.ACCENT)
        ax.tick_params(axis='x', colors=theme.TEXT_SECONDARY)
        ax.tick_params(axis='y', colors=theme.TEXT_SECONDARY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(theme.TEXT_SECONDARY)
        ax.spines['left'].set_color(theme.TEXT_SECONDARY)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def plot_pie_chart(self, parent):
        frame = tk.Frame(parent, bg=theme.BG_CARD)
        frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(frame, text="Time by Subject", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(pady=10)
        
        fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
        fig.patch.set_facecolor(theme.BG_CARD)
        
        if sum(self.subject_mins) > 0:
            colors = [theme.ACCENT, theme.ACCENT2, theme.SUCCESS, theme.WARNING, theme.DANGER]
            ax.pie(self.subject_mins, labels=self.subjects, autopct='%1.1f%%', colors=colors, textprops={'color': theme.TEXT_PRIMARY})
        else:
            ax.text(0.5, 0.5, "No Data", color=theme.TEXT_SECONDARY, ha="center", va="center")
            
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def draw_streak_calendar(self, parent):
        frame = tk.Frame(parent, bg=theme.BG_CARD)
        frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(frame, text="This Month Activity", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(pady=10)
        
        grid = tk.Frame(frame, bg=theme.BG_CARD)
        grid.pack(expand=True)
        
        # Fetch all active days this month
        uid = self.user_data['id']
        this_month = datetime.now().strftime("%Y-%m")
        res = database.fetch_all("SELECT DISTINCT date FROM sessions WHERE user_id=? AND date LIKE ?", (uid, f"{this_month}%"))
        active_days = [r['date'][-2:] for r in res]
        
        # Simple 5x7 grid
        day_counter = 1
        for row in range(5):
            for col in range(7):
                if day_counter > 31: break
                
                d_str = f"{day_counter:02d}"
                bg_col = theme.SUCCESS if d_str in active_days else theme.BG_MAIN
                fg_col = theme.TEXT_PRIMARY if d_str in active_days else theme.TEXT_SECONDARY
                
                tk.Label(grid, text=str(day_counter), bg=bg_col, fg=fg_col, width=3, height=1).grid(row=row, column=col, padx=2, pady=2)
                day_counter += 1
