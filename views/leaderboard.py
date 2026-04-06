import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import datetime
from styles import theme
from logic import database
from logic import utils
from logic import badges

class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, user_data, bg):
        super().__init__(parent, bg=bg)
        self.user_data = user_data
        self.bg = bg
        self.setup_ui()

    def setup_ui(self):
        lbl_title = tk.Label(self, text="Leaderboard & Profile", font=theme.FONT_TITLE, bg=self.bg, fg=theme.TEXT_PRIMARY)
        lbl_title.pack(anchor="w", padx=40, pady=(20, 10))
        
        style = ttk.Style()
        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=theme.BG_CARD, foreground=theme.TEXT_SECONDARY, padding=[20, 10], font=theme.FONT_BTN)
        style.map("TNotebook.Tab", background=[("selected", theme.ACCENT)], foreground=[("selected", theme.TEXT_PRIMARY)])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.tab_lb = tk.Frame(self.notebook, bg=self.bg)
        self.tab_prof = tk.Frame(self.notebook, bg=self.bg)
        
        self.notebook.add(self.tab_lb, text="Leaderboard")
        self.notebook.add(self.tab_prof, text="Your Profile")
        
        self.setup_lb_tab()
        self.setup_prof_tab()

    def setup_lb_tab(self):
        # Tools
        tools_frame = tk.Frame(self.tab_lb, bg=self.bg)
        tools_frame.pack(fill="x", pady=10)
        
        self.filter_var = tk.StringVar(value="Global")
        filters = ["Global", "Friends"]
        cb = ttk.Combobox(tools_frame, textvariable=self.filter_var, values=filters, state="readonly", font=theme.FONT_BODY)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda e: self.load_leaderboard())
        
        self.lb_container = tk.Frame(self.tab_lb, bg=self.bg)
        self.lb_container.pack(fill="both", expand=True, pady=10)
        
        self.load_leaderboard()

    def load_leaderboard(self):
        for w in self.lb_container.winfo_children(): w.destroy()
        
        filter_type = self.filter_var.get()
        if filter_type == "Global":
            q = "SELECT * FROM users ORDER BY xp DESC LIMIT 50"
            users = database.fetch_all(q)
        else:
            q = """
            SELECT u.* FROM users u 
            JOIN friends f ON (f.friend_id = u.id) 
            WHERE f.user_id = ? AND f.status='accepted'
            UNION
            SELECT * FROM users WHERE id = ?
            ORDER BY xp DESC LIMIT 50
            """
            users = database.fetch_all(q, (self.user_data['id'], self.user_data['id']))
            
        # Draw ranks
        for idx, u in enumerate(users):
            row = tk.Frame(self.lb_container, bg=theme.BG_CARD, height=60)
            
            # Colors for top 3
            rank_col = theme.TEXT_SECONDARY
            if idx == 0: rank_col = "#FFD700" # Gold
            elif idx == 1: rank_col = "#C0C0C0" # Silver
            elif idx == 2: rank_col = "#CD7F32" # Bronze
            
            tk.Label(row, text=f"#{idx+1}", font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=rank_col, width=4).place(x=10, y=15)
            
            # Avatar
            c = tk.Canvas(row, width=40, height=40, bg=theme.BG_CARD, highlightthickness=0)
            c.place(x=70, y=10)
            c.create_oval(2, 2, 38, 38, fill=u['avatar_color'], outline="")
            c.create_text(20, 20, text=u['display_name'][:2].upper(), font=("Helvetica", 14, "bold"), fill=theme.TEXT_PRIMARY)
            
            tk.Label(row, text=u['display_name'], font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).place(x=120, y=20)
            
            # Level & XP
            tk.Label(row, text=f"Lvl {u['level']}", font=theme.FONT_SMALL, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, padx=5).place(x=250, y=20)
            tk.Label(row, text=f"{u['xp']} XP", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.XP_COLOR).place(x=320, y=20)
            
            # Slide in animation
            target_y = idx * 65
            row.place(x=0, y=target_y + 100, width=700, height=60)
            self.after(idx * 50, lambda r=row, ty=target_y: self.slide_row(r, ty + 100, ty))

    def slide_row(self, row, curr_y, target_y):
        if not row.winfo_exists(): return
        if curr_y > target_y:
            step = max(5, int((curr_y - target_y) * 0.3))
            row.place(y=curr_y - step)
            self.after(20, lambda: self.slide_row(row, curr_y - step, target_y))
        else:
            row.place(y=target_y)

    def setup_prof_tab(self):
        usr = database.get_user_by_id(self.user_data['id'])
        if not usr: return
        
        # Top profile area
        top_frame = tk.Frame(self.tab_prof, bg=theme.BG_CARD, padx=20, pady=20)
        top_frame.pack(fill="x", pady=10)
        
        # Avatar
        c = tk.Canvas(top_frame, width=100, height=100, bg=theme.BG_CARD, highlightthickness=0)
        c.pack(side="left", padx=20)
        c.create_oval(5, 5, 95, 95, fill=usr['avatar_color'], outline="")
        c.create_text(50, 50, text=usr['display_name'][:2].upper(), font=("Helvetica", 32, "bold"), fill=theme.TEXT_PRIMARY)
        
        info_frame = tk.Frame(top_frame, bg=theme.BG_CARD)
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_frame, text=usr['display_name'], font=theme.FONT_TITLE, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(anchor="w")
        tk.Label(info_frame, text=f"Joined: {usr['created_at'][:10]}", font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(anchor="w")
        
        btn_edit = tk.Button(info_frame, text="Edit Name", font=theme.FONT_SMALL, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY, relief="flat", command=self.edit_name)
        btn_edit.pack(anchor="w", pady=10)
        
        # Stats Grid
        stats_frame = tk.Frame(self.tab_prof, bg=self.bg)
        stats_frame.pack(fill="x", pady=20)
        
        sess_c = database.fetch_one("SELECT COUNT(*) as c FROM sessions WHERE user_id=?", (usr['id'],))['c']
        task_c = database.fetch_one("SELECT COUNT(*) as c FROM tasks WHERE user_id=? AND is_done=1", (usr['id'],))['c']
        
        stat_items = [
            ("Total Hours", f"{usr['total_minutes']//60}h {usr['total_minutes']%60}m"),
            ("Sessions", str(sess_c)),
            ("Streak", f"🔥 {usr['streak']}"),
            ("Tasks Done", str(task_c))
        ]
        
        for i, (lbl, val) in enumerate(stat_items):
            bx = tk.Frame(stats_frame, bg=theme.BG_CARD, padx=20, pady=15)
            bx.grid(row=0, column=i, padx=10)
            tk.Label(bx, text=val, font=theme.FONT_TITLE, bg=theme.BG_CARD, fg=theme.ACCENT).pack()
            tk.Label(bx, text=lbl, font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack()
            
        # Badges
        tk.Label(self.tab_prof, text="Your Badges", font=theme.FONT_HEADING, bg=self.bg, fg=theme.TEXT_PRIMARY).pack(anchor="w", pady=10)
        badges_frame = tk.Frame(self.tab_prof, bg=theme.BG_CARD, padx=20, pady=20)
        badges_frame.pack(fill="both", expand=True)
        
        earned = [b['badge_key'] for b in database.get_user_badges(usr['id'])]
        
        row, col = 0, 0
        for key, bdata in badges.BADGES.items():
            is_earned = key in earned
            bg_col = theme.BG_MAIN if is_earned else "#2A2A3E"
            fg_col = theme.TEXT_PRIMARY if is_earned else theme.TEXT_SECONDARY
            emoji = bdata['emoji'] if is_earned else "🔒"
            
            b_card = tk.Frame(badges_frame, bg=bg_col, width=120, height=100)
            b_card.grid(row=row, column=col, padx=10, pady=10)
            b_card.grid_propagate(False)
            
            tk.Label(b_card, text=emoji, font=("Helvetica", 24), bg=bg_col, fg=fg_col).pack(pady=5)
            tk.Label(b_card, text=bdata['name'] if is_earned else "???", font=theme.FONT_SMALL, bg=bg_col, fg=fg_col).pack()
            
            col += 1
            if col > 4:
                col = 0
                row += 1

    def edit_name(self):
        new_name = simpledialog.askstring("Edit Name", "Enter new display name:")
        if new_name:
            database.execute_query("UPDATE users SET display_name=? WHERE id=?", (new_name, self.user_data['id']))
            self.setup_prof_tab() # Refresh
