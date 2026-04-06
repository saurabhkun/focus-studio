import tkinter as tk
from datetime import datetime
from styles import theme
from logic import utils
from views import settings
from views import timer
from views import planner
from views import music
from views import social
from views import leaderboard
from views import analytics

class AppWindow(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.title("FOCUS STUDIO")
        self.geometry("1100x700")
        self.configure(bg=theme.BG_MAIN)
        self.minsize(900, 600)
        
        self.current_frame = None
        self.nav_buttons = {}
        self.is_transitioning = False
        
        self.setup_ui()
        self.show_screen("timer")

    def setup_ui(self):
        # Base container
        self.main_container = tk.Frame(self, bg=theme.BG_MAIN)
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.main_container, bg=theme.BG_SIDEBAR, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Content Area
        self.content_area = tk.Frame(self.main_container, bg=theme.BG_MAIN)
        self.content_area.pack(side="left", fill="both", expand=True)
        
        self.setup_sidebar()
        self.setup_topbar()
        
        # Area where screens go
        self.screen_frame = tk.Frame(self.content_area, bg=theme.BG_MAIN)
        self.screen_frame.pack(fill="both", expand=True)

    def setup_sidebar(self):
        # Profile Section
        profile_frame = tk.Frame(self.sidebar, bg=theme.BG_SIDEBAR)
        profile_frame.pack(fill="x", pady=30)
        
        # Avatar (Circle using canvas)
        self.avatar_canvas = tk.Canvas(profile_frame, width=80, height=80, bg=theme.BG_SIDEBAR, highlightthickness=0)
        self.avatar_canvas.pack(pady=(0, 10))
        color = self.user_data.get('avatar_color', theme.ACCENT)
        self.avatar_canvas.create_oval(5, 5, 75, 75, fill=color, outline="")
        initials = self.user_data.get('display_name', 'U')[:2].upper()
        self.avatar_canvas.create_text(40, 40, text=initials, font=("Helvetica", 24, "bold"), fill=theme.TEXT_PRIMARY)
        
        # Username
        tk.Label(profile_frame, text=self.user_data.get('display_name', 'User'), font=theme.FONT_HEADING, bg=theme.BG_SIDEBAR, fg=theme.TEXT_PRIMARY).pack()
        
        # Level Badge
        lvl = self.user_data.get('level', 1)
        lvl_name = utils.get_level_name(lvl)
        tk.Label(profile_frame, text=f"Lvl {lvl} • {lvl_name}", font=theme.FONT_SMALL, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, padx=10, pady=2).pack(pady=(5, 15))
        
        # XP Bar
        xp = self.user_data.get('xp', 0)
        xp_needed = 200 # Simplified
        xp_pct = (xp % 200) / 200.0
        
        xp_frame = tk.Frame(profile_frame, bg=theme.BG_CARD, width=150, height=8)
        xp_frame.pack(pady=5)
        xp_frame.pack_propagate(False)
        tk.Frame(xp_frame, bg=theme.XP_COLOR, width=int(150 * xp_pct), height=8).pack(side="left", fill="y")
        
        # Navigation Links
        nav_items = [
            (" Timer", "timer"),
            (" Planner", "planner"),
            (" Music", "music"),
            (" Social", "social"),
            (" Leaderboard", "leaderboard"),
            (" Analytics", "analytics"),
            (" Settings", "settings")
        ]
        
        for text, key in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=theme.FONT_BTN, bg=theme.BG_SIDEBAR, fg=theme.TEXT_SECONDARY, relief="flat", anchor="w", padx=30, pady=10, command=lambda k=key: self.fade_to_screen(k))
            btn.pack(fill="x")
            # Bind hover
            btn.bind("<Enter>", lambda e, b=btn, k=key: self.on_nav_hover(b, k, True))
            btn.bind("<Leave>", lambda e, b=btn, k=key: self.on_nav_hover(b, k, False))
            self.nav_buttons[key] = btn

    def setup_topbar(self):
        self.topbar = tk.Frame(self.content_area, bg=theme.BG_CARD, height=60, padx=20)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        
        # Date
        today = datetime.now().strftime("%B %d, %Y")
        tk.Label(self.topbar, text=today, font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(side="left", pady=18)
        
        # Notifs
        self.notif_frame = tk.Frame(self.topbar, bg=theme.BG_CARD)
        self.notif_frame.pack(side="right", pady=15)
        
        streak = self.user_data.get('streak', 0)
        tk.Label(self.notif_frame, text=f"🔥 {streak}", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.WARNING).pack(side="left", padx=10)
        tk.Label(self.notif_frame, text="🔔 0", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(side="left", padx=10)

    def on_nav_hover(self, btn, key, is_hover):
        if getattr(self, "current_nav", None) == key:
            return
        btn.configure(bg=theme.BG_CARD if is_hover else theme.BG_SIDEBAR, fg=theme.TEXT_PRIMARY if is_hover else theme.TEXT_SECONDARY)

    def fade_to_screen(self, key):
        if getattr(self, "current_nav", None) == key or getattr(self, "is_transitioning", False):
            return
            
        # Highlight active
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=theme.ACCENT, fg=theme.TEXT_PRIMARY)
            else:
                btn.configure(bg=theme.BG_SIDEBAR, fg=theme.TEXT_SECONDARY)
        
        self.current_nav = key
        self.is_transitioning = True
        
        # Execute Alpha smooth fade out/in trick
        self.alpha_fade(0.9, key)

    def alpha_fade(self, alpha, key):
        if alpha > 0.0:
            self.attributes("-alpha", alpha)
            self.after(30, lambda: self.alpha_fade(alpha - 0.2, key))
        else:
            self.show_screen(key)
            self.alpha_fade_in(0.0)

    def alpha_fade_in(self, alpha):
        if alpha < 1.0:
            self.attributes("-alpha", alpha)
            self.after(30, lambda: self.alpha_fade_in(alpha + 0.2))
        else:
            self.attributes("-alpha", 1.0)
            self.is_transitioning = False

    def show_screen(self, key):
        if self.current_frame:
            self.current_frame.destroy()
            
        if key == "settings":
            self.current_frame = settings.SettingsScreen(self.screen_frame, self.user_data, self.destroy_and_logout)
        elif key == "timer":
            self.current_frame = timer.TimerScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        elif key == "planner":
            self.current_frame = planner.PlannerScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        elif key == "music":
            self.current_frame = music.MusicScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        elif key == "social":
            self.current_frame = social.SocialScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        elif key == "leaderboard":
            self.current_frame = leaderboard.LeaderboardScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        elif key == "analytics":
            self.current_frame = analytics.AnalyticsScreen(self.screen_frame, self.user_data, theme.BG_MAIN)
        else:
            self.current_frame = tk.Frame(self.screen_frame, bg=theme.BG_MAIN)
            
        self.current_frame.pack(fill="both", expand=True)

    def destroy_and_logout(self):
        self.destroy()
        from views import main
        mainapp = main.LoginApp()
        mainapp.mainloop()

if __name__ == "__main__":
    # Test shell launch
    test_user = {
        "display_name": "Test User",
        "username": "test",
        "avatar_color": theme.SUCCESS,
        "level": 3,
        "xp": 450,
        "streak": 5
    }
    app = AppWindow(test_user)
    app.mainloop()
