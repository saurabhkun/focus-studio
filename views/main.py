import tkinter as tk
from tkinter import messagebox
from styles import theme
from logic import auth
from views import settings
import random
import math

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FOCUS STUDIO - Login")
        self.geometry("450x600")
        self.configure(bg=theme.BG_MAIN)
        self.resizable(False, False)
        
        self.mode = "login" # "login" or "register"
        self.settings_data = settings.load_settings()
        self.setup_ui()

    def setup_ui(self):
        # Clear existing
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)
            
        for widget in self.winfo_children():
            widget.destroy()
            
        # Top Canvas for pulsating Logo
        self.logo_canvas = tk.Canvas(self, width=450, height=150, bg=theme.BG_MAIN, highlightthickness=0)
        self.logo_canvas.pack(pady=(40, 20))
        
        self.logo_text_id = self.logo_canvas.create_text(225, 75, text="🎯 FOCUS STUDIO", font=("Helvetica", 28, "bold"), fill=theme.ACCENT)
        self.scale_factor = 1.0
        self.scale_dir = 0.02
        
        # Form Container
        self.form_frame = tk.Frame(self, bg=theme.BG_CARD, padx=30, pady=30)
        self.form_frame.pack(fill="x", padx=40)
        
        title_text = "Welcome Back" if self.mode == "login" else "Create Account"
        tk.Label(self.form_frame, text=title_text, font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(pady=(0, 20))
        
        # Username
        tk.Label(self.form_frame, text="Username", font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(anchor="w")
        self.ent_username = tk.Entry(self.form_frame, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY)
        self.ent_username.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Password
        tk.Label(self.form_frame, text="Password", font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(anchor="w")
        self.ent_password = tk.Entry(self.form_frame, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY, show="*")
        self.ent_password.pack(fill="x", pady=(0, 25), ipady=5)
        
        if self.mode == "login":
            last_user = self.settings_data.get("last_username", "")
            if last_user:
                self.ent_username.insert(0, last_user)
        
        # Main Button
        btn_text = "Login" if self.mode == "login" else "Register"
        btn_cmd = self.do_login if self.mode == "login" else self.do_register
        
        btn_main = tk.Button(self.form_frame, text=btn_text, font=theme.FONT_BTN, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat", command=btn_cmd)
        btn_main.pack(fill="x", ipady=8)
        
        # Toggle Mode
        toggle_text = "Don't have an account? Register" if self.mode == "login" else "Already have an account? Login"
        btn_toggle = tk.Button(self, text=toggle_text, font=theme.FONT_SMALL, bg=theme.BG_MAIN, fg=theme.ACCENT2, relief="flat", activebackground=theme.BG_MAIN, activeforeground=theme.ACCENT, command=self.toggle_mode, bd=0)
        btn_toggle.pack(pady=20)
        
        self.animate_logo()

    def do_login(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        
        success, msg, user = auth.login(username, password)
        if success:
            # Save last username
            self.settings_data["last_username"] = username
            settings.save_settings(self.settings_data)
            
            self.destroy()
            from views import app
            app_win = app.AppWindow(user)
            app_win.mainloop()
        else:
            messagebox.showerror("Login Failed", msg)

    def do_register(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        
        colors = [theme.ACCENT, theme.ACCENT2, theme.WARNING, theme.SUCCESS, theme.DANGER]
        avatar_color = random.choice(colors)
        
        success, msg = auth.register(username, password, username, avatar_color)
        if success:
            messagebox.showinfo("Success", msg)
            self.mode = "login"
            self.setup_ui()
        else:
            messagebox.showerror("Error", msg)

    def toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.setup_ui()

    def animate_logo(self):
        try:
            self.scale_factor += self.scale_dir
            if self.scale_factor > 1.05 or self.scale_factor < 0.95:
                self.scale_dir *= -1
                
            y_offset = int(10 * math.sin(self.scale_factor * math.pi * 10))
            self.logo_canvas.coords(self.logo_text_id, 225, 75 + y_offset)
            
            self.after_id = self.after(50, self.animate_logo)
        except Exception:
            pass

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
