import customtkinter as ctk
from tkinter import messagebox
import random
import string
import webbrowser
from sqlite_viewer import SQLiteViewerWindow

from config import APP_NAME
from database import (
    create_tables,
    user_exists,
    add_credential,
    get_credentials,
    search_credentials,
    update_credential,
    delete_credential
)
from auth import register_master_password, login_master_password
from crypto_utils import encrypt_password, decrypt_password


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


SOCIAL_HANDLE = "@malredfan"
TWITTER_URL = "https://twitter.com/malredfan"
INSTAGRAM_URL = "https://instagram.com/malredfan"
LINKEDIN_URL = "https://www.linkedin.com/in/malredfan"


def open_social(url):
    webbrowser.open_new_tab(url)


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1100x700")
        self.minsize(1000, 650)

        self.encryption_key = None
        self.selected_credential_id = None

        create_tables()

        self.show_auth_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_auth_screen(self):
        self.clear_screen()

        container = ctk.CTkFrame(self, corner_radius=25)
        container.pack(expand=True, fill="both", padx=80, pady=60)

        left_frame = ctk.CTkFrame(container, fg_color="#111827", corner_radius=25)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=40, pady=40)

        title = ctk.CTkLabel(
            left_frame,
            text="Secure\nPassword\nManager",
            font=("Arial", 42, "bold"),
            text_color="#60A5FA",
            justify="left"
        )
        title.pack(anchor="w", padx=40, pady=(60, 20))

        subtitle = ctk.CTkLabel(
            left_frame,
            text="Store your credentials safely\nusing hashing and encryption.",
            font=("Arial", 18),
            text_color="#D1D5DB",
            justify="left"
        )
        subtitle.pack(anchor="w", padx=40)

        security_text = ctk.CTkLabel(
            left_frame,
            text="✓ bcrypt master password hashing\n✓ AES-based encryption\n✓ Local encrypted vault\n✓ SQLite secure storage",
            font=("Arial", 16),
            text_color="#A7F3D0",
            justify="left"
        )
        security_text.pack(anchor="w", padx=40, pady=(30, 20))

        social_title = ctk.CTkLabel(
            left_frame,
            text=f"Follow me:  {SOCIAL_HANDLE}",
            font=("Arial", 14, "bold"),
            text_color="#93C5FD"
        )
        social_title.pack(anchor="w", padx=40, pady=(5, 8))

        social_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        social_frame.pack(anchor="w", padx=40, pady=(0, 20))

        twitter_btn = ctk.CTkButton(
            social_frame,
            text="X",
            width=140,
            height=34,
            fg_color="#000000",
            hover_color="#000000",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(TWITTER_URL)
        )
        twitter_btn.pack(side="left", padx=(0, 8))

        instagram_btn = ctk.CTkButton(
            social_frame,
            text="Instagram",
            width=130,
            height=34,
            fg_color="#E1306C",
            hover_color="#B0245A",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(INSTAGRAM_URL)
        )
        instagram_btn.pack(side="left", padx=(0, 8))

        linkedin_btn = ctk.CTkButton(
            social_frame,
            text="LinkedIn",
            width=120,
            height=34,
            fg_color="#0A66C2",
            hover_color="#084E94",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(LINKEDIN_URL)
        )
        linkedin_btn.pack(side="left")


        if user_exists():
            header_text = "Login to Your Vault"
            button_text = "Login"
        else:
            header_text = "Create Master Password"
            button_text = "Create Vault"

        header = ctk.CTkLabel(
            right_frame,
            text=header_text,
            font=("Arial", 32, "bold")
        )
        header.pack(pady=(80, 20))

        self.master_password_entry = ctk.CTkEntry(
            right_frame,
            placeholder_text="Enter master password",
            show="*",
            width=360,
            height=45,
            font=("Arial", 15)
        )
        self.master_password_entry.pack(pady=15)

        self.auth_button = ctk.CTkButton(
            right_frame,
            text=button_text,
            height=45,
            width=360,
            font=("Arial", 16, "bold"),
            command=self.handle_auth
        )
        self.auth_button.pack(pady=20)

        note = ctk.CTkLabel(
            right_frame,
            text="Remember: If you forget the master password,\nyour stored passwords cannot be recovered.",
            font=("Arial", 13),
            text_color="#FCA5A5",
            justify="center"
        )
        note.pack(pady=20)

    def handle_auth(self):
        master_password = self.master_password_entry.get().strip()

        if not master_password:
            messagebox.showerror("Error", "Please enter a master password.")
            return

        if len(master_password) < 8:
            messagebox.showerror("Weak Password", "Master password must be at least 8 characters.")
            return

        if user_exists():
            key = login_master_password(master_password)

            if key:
                self.encryption_key = key
                self.show_dashboard()
            else:
                messagebox.showerror("Access Denied", "Incorrect master password.")
        else:
            key = register_master_password(master_password)
            self.encryption_key = key
            messagebox.showinfo("Success", "Vault created successfully.")
            self.show_dashboard()

    def show_dashboard(self):
        self.clear_screen()

        sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#0F172A")
        sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(
            sidebar,
            text="Password\nVault",
            font=("Arial", 30, "bold"),
            text_color="#60A5FA",
            justify="left"
        )
        title.pack(anchor="w", padx=30, pady=(40, 20))

        menu_text = ctk.CTkLabel(
            sidebar,
            text="Secure Local Manager",
            font=("Arial", 14),
            text_color="#CBD5E1"
        )
        menu_text.pack(anchor="w", padx=30, pady=(0, 30))

        add_btn = ctk.CTkButton(
            sidebar,
            text="Add Credential",
            height=42,
            command=self.clear_form
        )
        add_btn.pack(fill="x", padx=25, pady=10)

        refresh_btn = ctk.CTkButton(
            sidebar,
            text="Refresh Vault",
            height=42,
            command=self.load_credentials
        )
        refresh_btn.pack(fill="x", padx=25, pady=10)

        database_btn = ctk.CTkButton(
            sidebar,
            text="View SQLite Data",
            height=42,
            fg_color="#7C3AED",
            hover_color="#5B21B6",
            command=self.open_sqlite_viewer
        )
        database_btn.pack(fill="x", padx=25, pady=10)

        logout_btn = ctk.CTkButton(
            sidebar,
            text="Logout",
            height=42,
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=self.show_auth_screen
        )
        logout_btn.pack(fill="x", padx=25, pady=10)

        # ====== روابط التواصل الاجتماعي (أسفل الشريط الجانبي) ======
        social_container = ctk.CTkFrame(
            sidebar,
            fg_color="#111827",
            corner_radius=15
        )
        social_container.pack(side="bottom", fill="x", padx=15, pady=15)

        social_header = ctk.CTkLabel(
            social_container,
            text=f"Follow  {SOCIAL_HANDLE}",
            font=("Arial", 13, "bold"),
            text_color="#93C5FD"
        )
        social_header.pack(pady=(12, 8))

        twitter_btn = ctk.CTkButton(
            social_container,
            text="🐦 Twitter / X",
            height=34,
            fg_color="#1DA1F2",
            hover_color="#0D8BD9",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(TWITTER_URL)
        )
        twitter_btn.pack(fill="x", padx=12, pady=4)

        instagram_btn = ctk.CTkButton(
            social_container,
            text="📷 Instagram",
            height=34,
            fg_color="#E1306C",
            hover_color="#B0245A",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(INSTAGRAM_URL)
        )
        instagram_btn.pack(fill="x", padx=12, pady=4)

        linkedin_btn = ctk.CTkButton(
            social_container,
            text="💼 LinkedIn",
            height=34,
            fg_color="#0A66C2",
            hover_color="#084E94",
            font=("Arial", 12, "bold"),
            command=lambda: open_social(LINKEDIN_URL)
        )
        linkedin_btn.pack(fill="x", padx=12, pady=(4, 12))

        # ====== نهاية قسم السوشيال ======

        main_area = ctk.CTkFrame(self, fg_color="#020617")
        main_area.pack(side="right", fill="both", expand=True)

        top_bar = ctk.CTkFrame(main_area, height=90, fg_color="#020617")
        top_bar.pack(fill="x", padx=25, pady=(20, 5))

        heading = ctk.CTkLabel(
            top_bar,
            text="Encrypted Credentials",
            font=("Arial", 30, "bold")
        )
        heading.pack(side="left", padx=10)

        self.search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search website or username...",
            width=300,
            height=40
        )
        self.search_entry.pack(side="right", padx=10)

        search_btn = ctk.CTkButton(
            top_bar,
            text="Search",
            width=100,
            height=40,
            command=self.search_data
        )
        search_btn.pack(side="right", padx=5)

        content = ctk.CTkFrame(main_area, fg_color="#020617")
        content.pack(fill="both", expand=True, padx=25, pady=10)

        form_frame = ctk.CTkFrame(content, width=360, corner_radius=20, fg_color="#111827")
        form_frame.pack(side="left", fill="y", padx=(0, 20), pady=10)

        form_title = ctk.CTkLabel(
            form_frame,
            text="Credential Details",
            font=("Arial", 22, "bold")
        )
        form_title.pack(pady=(25, 15))

        self.website_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Website / App Name",
            width=300,
            height=42
        )
        self.website_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Username / Email",
            width=300,
            height=42
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Password",
            width=300,
            height=42,
            show="*"
        )
        self.password_entry.pack(pady=10)

        generate_btn = ctk.CTkButton(
            form_frame,
            text="Generate Strong Password",
            width=300,
            height=38,
            fg_color="#2563EB",
            command=self.generate_password
        )
        generate_btn.pack(pady=8)

        self.notes_entry = ctk.CTkTextbox(
            form_frame,
            width=300,
            height=90
        )
        self.notes_entry.pack(pady=10)
        self.notes_entry.insert("1.0", "Notes")

        save_btn = ctk.CTkButton(
            form_frame,
            text="Save Credential",
            width=300,
            height=42,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.save_credential
        )
        save_btn.pack(pady=(15, 8))

        update_btn = ctk.CTkButton(
            form_frame,
            text="Update Selected",
            width=300,
            height=42,
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self.update_selected
        )
        update_btn.pack(pady=8)

        delete_btn = ctk.CTkButton(
            form_frame,
            text="Delete Selected",
            width=300,
            height=42,
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=self.delete_selected
        )
        delete_btn.pack(pady=8)

        self.list_frame = ctk.CTkScrollableFrame(
            content,
            corner_radius=20,
            fg_color="#111827"
        )
        self.list_frame.pack(side="right", fill="both", expand=True, pady=10)

        self.load_credentials()

    def save_credential(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end").strip()

        if not website or not username or not password:
            messagebox.showerror("Error", "Website, username, and password are required.")
            return

        encrypted_password = encrypt_password(password, self.encryption_key)

        add_credential(
            website,
            username,
            encrypted_password,
            notes
        )

        messagebox.showinfo("Success", "Credential saved securely.")
        self.clear_form()
        self.load_credentials()

    def load_credentials(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        credentials = get_credentials()

        if not credentials:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No credentials saved yet.",
                font=("Arial", 18),
                text_color="#94A3B8"
            )
            empty_label.pack(pady=40)
            return

        for item in credentials:
            self.create_credential_card(item)

    def create_credential_card(self, item):
        credential_id, website, username, encrypted_password, notes, created_at = item

        card = ctk.CTkFrame(
            self.list_frame,
            corner_radius=18,
            fg_color="#1E293B"
        )
        card.pack(fill="x", padx=15, pady=10)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15, 5))

        website_label = ctk.CTkLabel(
            top,
            text=website,
            font=("Arial", 20, "bold"),
            text_color="#60A5FA"
        )
        website_label.pack(side="left")

        date_label = ctk.CTkLabel(
            top,
            text=str(created_at),
            font=("Arial", 12),
            text_color="#94A3B8"
        )
        date_label.pack(side="right")

        username_label = ctk.CTkLabel(
            card,
            text=f"Username: {username}",
            font=("Arial", 14),
            text_color="#E5E7EB"
        )
        username_label.pack(anchor="w", padx=20, pady=3)

        try:
            decrypted_password = decrypt_password(encrypted_password, self.encryption_key)
        except Exception:
            decrypted_password = "Unable to decrypt"

        password_label = ctk.CTkLabel(
            card,
            text=f"Password: {decrypted_password}",
            font=("Arial", 14),
            text_color="#A7F3D0"
        )
        password_label.pack(anchor="w", padx=20, pady=3)

        if notes:
            notes_label = ctk.CTkLabel(
                card,
                text=f"Notes: {notes}",
                font=("Arial", 13),
                text_color="#CBD5E1",
                wraplength=600,
                justify="left"
            )
            notes_label.pack(anchor="w", padx=20, pady=3)

        select_btn = ctk.CTkButton(
            card,
            text="Select",
            width=120,
            height=35,
            command=lambda: self.select_credential(
                credential_id,
                website,
                username,
                decrypted_password,
                notes
            )
        )
        select_btn.pack(anchor="e", padx=20, pady=(5, 15))

    def select_credential(self, credential_id, website, username, password, notes):
        self.selected_credential_id = credential_id

        self.website_entry.delete(0, "end")
        self.website_entry.insert(0, website)

        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, username)

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.notes_entry.delete("1.0", "end")
        self.notes_entry.insert("1.0", notes if notes else "")

    def update_selected(self):
        if not self.selected_credential_id:
            messagebox.showerror("Error", "Please select a credential first.")
            return

        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end").strip()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        encrypted_password = encrypt_password(password, self.encryption_key)

        update_credential(
            self.selected_credential_id,
            website,
            username,
            encrypted_password,
            notes
        )

        messagebox.showinfo("Success", "Credential updated successfully.")
        self.clear_form()
        self.load_credentials()

    def delete_selected(self):
        if not self.selected_credential_id:
            messagebox.showerror("Error", "Please select a credential first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this credential?"
        )

        if confirm:
            delete_credential(self.selected_credential_id)
            messagebox.showinfo("Deleted", "Credential deleted successfully.")
            self.clear_form()
            self.load_credentials()

    def search_data(self):
        keyword = self.search_entry.get().strip()

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if keyword:
            results = search_credentials(keyword)
        else:
            results = get_credentials()

        if not results:
            label = ctk.CTkLabel(
                self.list_frame,
                text="No results found.",
                font=("Arial", 18),
                text_color="#94A3B8"
            )
            label.pack(pady=40)
            return

        for item in results:
            self.create_credential_card(item)

    def clear_form(self):
        self.selected_credential_id = None

        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.notes_entry.delete("1.0", "end")

    def generate_password(self):
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}"

        password = "".join(random.choice(characters) for _ in range(length))

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def open_sqlite_viewer(self):
        SQLiteViewerWindow(self)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()