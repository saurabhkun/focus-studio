import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
from styles import theme
from logic import database
import random
import string

class SocialScreen(tk.Frame):
    def __init__(self, parent, user_data, bg):
        super().__init__(parent, bg=bg)
        self.user_data = user_data
        self.bg = bg
        self.setup_ui()

    def setup_ui(self):
        lbl_title = tk.Label(self, text="Social Hub", font=theme.FONT_TITLE, bg=self.bg, fg=theme.TEXT_PRIMARY)
        lbl_title.pack(anchor="w", padx=40, pady=(20, 10))
        
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=theme.BG_CARD, foreground=theme.TEXT_SECONDARY, padding=[20, 10], font=theme.FONT_BTN)
        style.map("TNotebook.Tab", background=[("selected", theme.ACCENT)], foreground=[("selected", theme.TEXT_PRIMARY)])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Tabs
        self.tab_friends = tk.Frame(self.notebook, bg=self.bg)
        self.tab_dm = tk.Frame(self.notebook, bg=self.bg)
        self.tab_classes = tk.Frame(self.notebook, bg=self.bg)
        
        self.notebook.add(self.tab_friends, text="Friends")
        self.notebook.add(self.tab_dm, text="Direct Messages")
        self.notebook.add(self.tab_classes, text="Classrooms")
        
        self.setup_friends_tab()
        self.setup_dm_tab()
        self.setup_classes_tab()

    # --- FRIENDS TAB ---
    def setup_friends_tab(self):
        # Top search
        search_frame = tk.Frame(self.tab_friends, bg=self.bg)
        search_frame.pack(fill="x", pady=20)
        
        self.ent_search = tk.Entry(search_frame, font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY)
        self.ent_search.pack(side="left", fill="x", expand=True, ipady=5)
        
        btn_search = tk.Button(search_frame, text="Add Friend", font=theme.FONT_BTN, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat", command=self.add_friend)
        btn_search.pack(side="left", padx=10)
        
        # Lists
        tk.Label(self.tab_friends, text="Your Friends", font=theme.FONT_HEADING, bg=self.bg, fg=theme.TEXT_PRIMARY).pack(anchor="w", pady=(10, 5))
        self.friends_list_frame = tk.Frame(self.tab_friends, bg=theme.BG_CARD)
        self.friends_list_frame.pack(fill="both", expand=True)
        self.load_friends()

    def add_friend(self):
        username = self.ent_search.get().strip()
        if not username: return
        target = database.get_user_by_username(username)
        if target:
            if target['id'] == self.user_data['id']:
                messagebox.showinfo("Wait", "You can't add yourself.")
                return
            
            # Since mock system offline, auto accept
            database.execute_query("INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, ?)", (self.user_data['id'], target['id'], "accepted"))
            database.execute_query("INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, ?)", (target['id'], self.user_data['id'], "accepted"))
            messagebox.showinfo("Success", f"{username} added as friend!")
            
            # Badge
            database.add_badge(self.user_data['id'], "social_1")
            self.load_friends()
        else:
            messagebox.showerror("Error", "User not found.")

    def load_friends(self):
        for w in self.friends_list_frame.winfo_children(): w.destroy()
        
        q = "SELECT u.id, u.username, u.display_name FROM friends f JOIN users u ON f.friend_id = u.id WHERE f.user_id = ? AND f.status='accepted'"
        friends = database.fetch_all(q, (self.user_data['id'],))
        
        if not friends:
            tk.Label(self.friends_list_frame, text="No friends yet.", fg=theme.TEXT_SECONDARY, bg=theme.BG_CARD, font=theme.FONT_BODY).pack(pady=20)
            return

        for f in friends:
            row = tk.Frame(self.friends_list_frame, bg=theme.BG_CARD)
            row.pack(fill="x", pady=5, padx=10)
            
            # Online indicator (randomized mock)
            is_online = random.choice([True, False])
            color = theme.SUCCESS if is_online else theme.TEXT_SECONDARY
            
            tk.Label(row, text="●", fg=color, bg=theme.BG_CARD, font=("Helvetica", 14)).pack(side="left", padx=5)
            tk.Label(row, text=f['display_name'], font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(side="left")
            
            btn_msg = tk.Button(row, text="Message", font=theme.FONT_SMALL, bg=theme.ACCENT2, fg=theme.TEXT_PRIMARY, relief="flat", command=lambda fid=f['id']: self.open_dm(fid))
            btn_msg.pack(side="right")

    # --- DMs TAB ---
    def setup_dm_tab(self):
        # We need a pane: left side friend list, right side chat
        paned = tk.PanedWindow(self.tab_dm, orient="horizontal", bg=theme.BG_CARD, sashwidth=5)
        paned.pack(fill="both", expand=True, pady=10)
        
        left_frame = tk.Frame(paned, bg=theme.BG_CARD, width=150)
        paned.add(left_frame, minsize=150)
        
        self.right_frame = tk.Frame(paned, bg=self.bg)
        paned.add(self.right_frame)
        
        tk.Label(left_frame, text="Conversations", font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(pady=10)
        
        q = "SELECT DISTINCT u.id, u.username, u.display_name FROM friends f JOIN users u ON f.friend_id = u.id WHERE f.user_id = ?"
        friends = database.fetch_all(q, (self.user_data['id'],))
        
        for f in friends:
            btn = tk.Button(left_frame, text=f['display_name'], font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, relief="flat", anchor="w", command=lambda fid=f['id']: self.open_dm(fid))
            btn.pack(fill="x", padx=10, pady=2)
            
        self.chat_canvas = tk.Canvas(self.right_frame, bg=self.bg, highlightthickness=0)
        self.chat_canvas.pack(fill="both", expand=True, pady=(0, 10))
        self.chat_inner = tk.Frame(self.chat_canvas, bg=self.bg)
        self.chat_canvas.create_window((0, 0), window=self.chat_inner, anchor="nw", width=600)
        
        self.msg_entry = tk.Entry(self.right_frame, font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, insertbackground=theme.TEXT_PRIMARY)
        self.msg_entry.pack(side="left", fill="x", expand=True, ipady=5)
        
        self.btn_send = tk.Button(self.right_frame, text="Send", font=theme.FONT_BTN, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat")
        self.btn_send.pack(side="left", padx=10)

    def open_dm(self, friend_id):
        self.notebook.select(self.tab_dm)
        self.current_chat_id = friend_id
        
        self.btn_send.configure(command=lambda: self.send_message(friend_id))
        self.load_messages()

    def send_message(self, friend_id):
        txt = self.msg_entry.get().strip()
        if not txt: return
        now = datetime.now().isoformat()
        database.execute_query("INSERT INTO messages (sender_id, receiver_id, content, sent_at) VALUES (?, ?, ?, ?)",
                              (self.user_data['id'], friend_id, txt, now))
        self.msg_entry.delete(0, tk.END)
        self.load_messages()

    def load_messages(self):
        for w in self.chat_inner.winfo_children(): w.destroy()
        
        q = "SELECT * FROM messages WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?) ORDER BY sent_at ASC"
        msgs = database.fetch_all(q, (self.user_data['id'], self.current_chat_id, self.current_chat_id, self.user_data['id']))
        
        for m in msgs:
            is_me = (m['sender_id'] == self.user_data['id'])
            bg_col = theme.ACCENT if is_me else theme.BG_CARD
            anchor = "e" if is_me else "w"
            
            row = tk.Frame(self.chat_inner, bg=self.bg)
            row.pack(fill="x", pady=5)
            
            bubble = tk.Label(row, text=m['content'], font=theme.FONT_BODY, bg=bg_col, fg=theme.TEXT_PRIMARY, wraplength=400, justify="left", padx=15, pady=10)
            bubble.pack(side="right" if is_me else "left", padx=20)
            
        self.chat_inner.update_idletasks()
        self.chat_canvas.yview_moveto(1.0) # auto scroll

    # --- CLASSROOMS TAB ---
    def setup_classes_tab(self):
        top_frame = tk.Frame(self.tab_classes, bg=self.bg)
        top_frame.pack(fill="x", pady=20)
        
        btn_create = tk.Button(top_frame, text="+ Create Classroom", font=theme.FONT_BTN, bg=theme.SUCCESS, fg=theme.TEXT_PRIMARY, relief="flat", command=self.create_class)
        btn_create.pack(side="left", padx=10)
        
        btn_join = tk.Button(top_frame, text="Join with Code", font=theme.FONT_BTN, bg=theme.ACCENT, fg=theme.TEXT_PRIMARY, relief="flat", command=self.join_class)
        btn_join.pack(side="left", padx=10)
        
        self.class_list_frame = tk.Frame(self.tab_classes, bg=self.bg)
        self.class_list_frame.pack(fill="both", expand=True)
        self.load_classes()

    def create_class(self):
        name = simpledialog.askstring("New Classroom", "Classroom Name:")
        if name:
            sub = simpledialog.askstring("Subject", "Subject:")
            if sub:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                cid = database.execute_query("INSERT INTO classrooms (name, subject, created_by, join_code, created_at) VALUES (?, ?, ?, ?, ?)",
                                      (name, sub, self.user_data['id'], code, datetime.now().isoformat()))
                database.execute_query("INSERT INTO classroom_members (classroom_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)",
                                      (cid, self.user_data['id'], "admin", datetime.now().isoformat()))
                self.load_classes()
                messagebox.showinfo("Created", f"Classroom created!\nJoin Code: {code}")

    def join_class(self):
        code = simpledialog.askstring("Join", "Enter 6-character Join Code:")
        if code:
            cls = database.fetch_one("SELECT * FROM classrooms WHERE join_code=?", (code.upper(),))
            if cls:
                database.execute_query("INSERT INTO classroom_members (classroom_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)",
                                      (cls['id'], self.user_data['id'], "member", datetime.now().isoformat()))
                self.load_classes()
            else:
                messagebox.showerror("Error", "Invalid code.")

    def load_classes(self):
        for w in self.class_list_frame.winfo_children(): w.destroy()
        
        q = "SELECT c.* FROM classrooms c JOIN classroom_members cm ON c.id=cm.classroom_id WHERE cm.user_id=?"
        classes = database.fetch_all(q, (self.user_data['id'],))
        
        if not classes:
            tk.Label(self.class_list_frame, text="You haven't joined any classrooms.", fg=theme.TEXT_SECONDARY, bg=self.bg, font=theme.FONT_BODY).pack(pady=20)
            return
            
        for c in classes:
            card = tk.Frame(self.class_list_frame, bg=theme.BG_CARD, padx=20, pady=15)
            card.pack(fill="x", pady=5, padx=10)
            
            tk.Label(card, text=c['name'], font=theme.FONT_HEADING, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY).pack(side="left")
            tk.Label(card, text=f"• {c['subject']}", font=theme.FONT_BODY, bg=theme.BG_CARD, fg=theme.ACCENT2).pack(side="left", padx=10)
            tk.Label(card, text=f"Code: {c['join_code']}", font=theme.FONT_SMALL, bg=theme.BG_CARD, fg=theme.TEXT_SECONDARY).pack(side="right")
