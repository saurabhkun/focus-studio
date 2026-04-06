import tkinter as tk
from tkinter import ttk
import os
import random
import pygame
from styles import theme
from views import settings

class MusicScreen(tk.Frame):
    def __init__(self, parent, user_data, bg):
        super().__init__(parent, bg=bg)
        self.user_data = user_data
        self.settings = settings.load_settings()
        
        pygame.mixer.init()
        
        self.music_dir = self.settings.get("music_folder", "")
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        
        self.vinyl_angle = 0
        self.marquee_offset = 0
        self.eq_bars_ids = []
        
        self.load_playlist()
        self.setup_ui()

    def load_playlist(self):
        if not self.music_dir or not os.path.exists(self.music_dir):
            return
            
        for f in os.listdir(self.music_dir):
            if f.lower().endswith(".mp3"):
                self.playlist.append(os.path.join(self.music_dir, f))

    def setup_ui(self):
        lbl_title = tk.Label(self, text="Music Player", font=theme.FONT_TITLE, bg=theme.BG_MAIN, fg=theme.TEXT_PRIMARY)
        lbl_title.pack(anchor="w", padx=40, pady=(20, 10))
        
        if not self.playlist:
            msg = "No MP3 files found.\nPlease check your Music Folder in Settings."
            if not self.music_dir:
                msg = "Music folder not configured.\nPlease go to Settings and select a directory containing MP3 files."
            tk.Label(self, text=msg, font=theme.FONT_BODY, bg=theme.BG_MAIN, fg=theme.TEXT_SECONDARY, justify="left").pack(anchor="w", padx=40, pady=20)
            return

        # Player Container
        container = tk.Frame(self, bg=theme.BG_CARD, padx=20, pady=20)
        container.pack(fill="x", padx=40, pady=10)
        
        # Animations Canvas (Top part)
        self.canvas = tk.Canvas(container, height=120, bg=theme.BG_CARD, highlightthickness=0)
        self.canvas.pack(fill="x")
        
        # Vinyl record
        self.canvas.create_oval(10, 10, 110, 110, fill="black", outline="")
        self.vinyl_arc = self.canvas.create_arc(10, 10, 110, 110, start=0, extent=45, fill="gray25", outline="")
        self.canvas.create_oval(50, 50, 70, 70, fill=theme.ACCENT, outline="", tags="vinyl_center")
        
        # EQ Bars
        eq_x = 150
        self.eq_bars_ids = []
        for i in range(5):
            bar = self.canvas.create_rectangle(eq_x + (i*20), 100, eq_x + (i*20) + 10, 100, fill=theme.ACCENT2, outline="")
            self.eq_bars_ids.append(bar)
            
        # Marquee Title
        self.title_var = tk.StringVar(value="Ready to play")
        self.lbl_title = tk.Label(container, textvariable=self.title_var, font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, width=30, anchor="w")
        self.lbl_title.pack(pady=(10, 5))
        
        # Progress Bar Canvas
        self.prog_canvas = tk.Canvas(container, height=10, bg=theme.BG_CARD, highlightthickness=0)
        self.prog_canvas.pack(fill="x", pady=5)
        self.prog_bg = self.prog_canvas.create_rectangle(0, 4, 3000, 6, fill=theme.BG_MAIN, outline="")
        self.prog_fg = self.prog_canvas.create_rectangle(0, 4, 0, 6, fill=theme.ACCENT, outline="")
        
        # Controls Frame
        ctrl_frame = tk.Frame(container, bg=theme.BG_CARD)
        ctrl_frame.pack(pady=10)
        
        btn_prev = tk.Button(ctrl_frame, text="⏮", font=("Helvetica", 16), bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, relief="flat", command=self.prev_song)
        btn_prev.pack(side="left", padx=5)
        
        self.btn_play = tk.Button(ctrl_frame, text="▶", font=("Helvetica", 20), bg=theme.BG_CARD, fg=theme.ACCENT, relief="flat", command=self.toggle_play)
        self.btn_play.pack(side="left", padx=15)
        
        btn_next = tk.Button(ctrl_frame, text="⏭", font=("Helvetica", 16), bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, relief="flat", command=self.next_song)
        btn_next.pack(side="left", padx=5)
        
        # Volume
        vol_frame = tk.Frame(container, bg=theme.BG_CARD)
        vol_frame.pack(pady=5)
        self.vol_slider = ttk.Scale(vol_frame, from_=0, to=1, orient="horizontal", command=self.set_volume)
        self.vol_slider.set(0.5)
        self.vol_slider.pack()
        
        # Animations Loops
        self.animate_vinyl()
        self.animate_eq()
        self.animate_marquee()
        self.update_progress()

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def get_current_song_name(self):
        if not self.playlist:
            return ""
        return os.path.basename(self.playlist[self.current_index])

    def toggle_play(self):
        if not self.playlist:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.btn_play.configure(text="▶")
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.playlist[self.current_index])
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            self.is_playing = True
            self.btn_play.configure(text="⏸")
            
        self.marquee_offset = 0
            
    def next_song(self):
        if not self.playlist: return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_current()
        
    def prev_song(self):
        if not self.playlist: return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_current()
        
    def play_current(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.btn_play.configure(text="⏸")
        self.marquee_offset = 0

    def animate_vinyl(self):
        if self.is_playing:
            self.vinyl_angle = (self.vinyl_angle - 3) % 360
            self.canvas.itemconfig(self.vinyl_arc, start=self.vinyl_angle)
            
            # Glow pulse
            col = theme.ACCENT2 if (self.vinyl_angle % 30) < 15 else theme.ACCENT
            self.canvas.itemconfig("vinyl_center", fill=col)
            
        self.after(50, self.animate_vinyl)

    def animate_eq(self):
        if self.is_playing:
            for bar in self.eq_bars_ids:
                h = random.randint(10, 60)
                coords = self.canvas.coords(bar)
                self.canvas.coords(bar, coords[0], 100-h, coords[2], 100)
        else:
            for bar in self.eq_bars_ids:
                coords = self.canvas.coords(bar)
                self.canvas.coords(bar, coords[0], 98, coords[2], 100)
                
        self.after(150, self.animate_eq)

    def animate_marquee(self):
        if self.is_playing:
            full_name = self.get_current_song_name() + "   ***   "
            if len(full_name) > 30:
                disp = full_name[self.marquee_offset:] + full_name[:self.marquee_offset]
                self.title_var.set(disp[:30])
                self.marquee_offset = (self.marquee_offset + 1) % len(full_name)
            else:
                self.title_var.set(full_name.replace("   ***   ", ""))
        else:
            name = self.get_current_song_name()
            self.title_var.set(name[:30] if name else "Ready to play")
            
        self.after(200, self.animate_marquee)

    def update_progress(self):
        if self.is_playing and pygame.mixer.music.get_busy():
            # In simple terms without a complex track length reader, we mock progress or use get_pos
            pos = pygame.mixer.music.get_pos()
            # For pure simulation, assume a 3 min track if we cant read metadata easily w/o mutagen
            # MP3 length requires external libs, so we just loop a 3 min bar
            est_length = 3 * 60 * 1000
            pct = min(1.0, (pos % est_length) / est_length)
            w = self.prog_canvas.winfo_width()
            self.prog_canvas.coords(self.prog_fg, 0, 4, int(w * pct), 6)
            
        self.after(500, self.update_progress)
