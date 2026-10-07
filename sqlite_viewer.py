import customtkinter as ctk
from database import get_connection


class SQLiteViewerWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("SQLite Database Viewer")
        self.geometry("950x600")
        self.minsize(850, 500)

        self.configure(fg_color="#020617")

        title = ctk.CTkLabel(
            self,
            text="SQLite Database Viewer",
            font=("Arial", 28, "bold"),
            text_color="#60A5FA"
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="This window displays stored data directly from the SQLite database.",
            font=("Arial", 14),
            text_color="#CBD5E1"
        )
        subtitle.pack(pady=(0, 15))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        users_btn = ctk.CTkButton(
            button_frame,
            text="View Users Table",
            width=180,
            height=40,
            command=self.show_users_table
        )
        users_btn.pack(side="left", padx=10)

        credentials_btn = ctk.CTkButton(
            button_frame,
            text="View Credentials Table",
            width=200,
            height=40,
            command=self.show_credentials_table
        )
        credentials_btn.pack(side="left", padx=10)

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="Refresh",
            width=120,
            height=40,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.show_credentials_table
        )
        refresh_btn.pack(side="left", padx=10)

        self.table_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#111827",
            corner_radius=18
        )
        self.table_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.show_credentials_table()

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def create_cell(self, parent, text, row, column, width=160, is_header=False):
        label = ctk.CTkLabel(
            parent,
            text=str(text),
            width=width,
            height=35,
            corner_radius=8,
            fg_color="#1E293B" if not is_header else "#2563EB",
            text_color="#E5E7EB",
            font=("Arial", 13, "bold") if is_header else ("Arial", 12),
            wraplength=width - 10
        )
        label.grid(row=row, column=column, padx=4, pady=4, sticky="nsew")

    def show_users_table(self):
        self.clear_table()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, master_hash, salt FROM users")
        rows = cursor.fetchall()

        conn.close()

        headers = ["ID", "Master Hash", "Salt"]

        for col, header in enumerate(headers):
            self.create_cell(
                self.table_frame,
                header,
                0,
                col,
                width=260 if col != 0 else 80,
                is_header=True
            )

        if not rows:
            empty_label = ctk.CTkLabel(
                self.table_frame,
                text="No data found in users table.",
                font=("Arial", 16),
                text_color="#94A3B8"
            )
            empty_label.grid(row=1, column=0, columnspan=3, pady=30)
            return

        for row_index, row_data in enumerate(rows, start=1):
            user_id, master_hash, salt = row_data

            self.create_cell(self.table_frame, user_id, row_index, 0, width=80)
            self.create_cell(self.table_frame, master_hash, row_index, 1, width=360)
            self.create_cell(self.table_frame, salt, row_index, 2, width=360)

    def show_credentials_table(self):
        self.clear_table()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, website, username, password, notes, created_at
            FROM credentials
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        headers = ["ID", "Website", "Username", "Encrypted Password", "Notes", "Created At"]

        widths = [60, 140, 180, 300, 180, 160]

        for col, header in enumerate(headers):
            self.create_cell(
                self.table_frame,
                header,
                0,
                col,
                width=widths[col],
                is_header=True
            )

        if not rows:
            empty_label = ctk.CTkLabel(
                self.table_frame,
                text="No data found in credentials table.",
                font=("Arial", 16),
                text_color="#94A3B8"
            )
            empty_label.grid(row=1, column=0, columnspan=6, pady=30)
            return

        for row_index, row_data in enumerate(rows, start=1):
            for col_index, value in enumerate(row_data):
                self.create_cell(
                    self.table_frame,
                    value,
                    row_index,
                    col_index,
                    width=widths[col_index]
                )