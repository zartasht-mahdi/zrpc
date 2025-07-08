import tkinter as tk
from tkinter import messagebox, ttk
import os
import time
from pypresence import Presence

PROFILE_DIR = "profiles"

if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

class ZRPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZRPC - Rich Presence Launcher")
        self.root.configure(bg="#f0f0f0")
        self.current_profile = tk.StringVar()
        self.profile_names = []
        self.rpc = None

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TEntry", padding=6, relief="flat", borderwidth=1)
        style.configure("TButton", padding=6, relief="flat", borderwidth=0, background="#4CAF50", foreground="white")
        style.map("TButton", background=[('active', '#45a049')])

        tk.Label(root, text="Select Profile:", bg="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.profile_menu = ttk.Combobox(root, textvariable=self.current_profile, width=47)
        self.profile_menu.grid(row=0, column=1, padx=5, pady=5)
        self.profile_menu.bind("<<ComboboxSelected>>", self.load_profile)

        self.load_profile_names()

        row = 1
        self.entries = {}
        fields = [
            ("ClientID", "client_id"),
            ("Description Line 1", "details"),
            ("Description Line 2", "state"),
            ("LargeImage", "large_image"),
            ("LargeImageTooltip", "large_tooltip"),
            ("SmallImage", "small_image"),
            ("SmallImageTooltip", "small_tooltip"),
        ]
        for label, key in fields:
            tk.Label(root, text=label + ":", bg="#f0f0f0").grid(row=row, column=0, sticky="e")
            entry = ttk.Entry(root, width=50)
            entry.grid(row=row, column=1, padx=4, pady=4)
            self.entries[key] = entry
            row += 1

        # Time input
        tk.Label(root, text="How long ago did you start?", bg="#f0f0f0").grid(row=row, column=0, sticky="e")
        self.time_value_entry = ttk.Entry(root, width=50)
        self.time_value_entry.grid(row=row, column=1, padx=4, pady=4)
        row += 1

        tk.Label(root, text="Enter time in:", bg="#f0f0f0").grid(row=row, column=0, sticky="e")
        self.time_unit = tk.StringVar(value="Hours")
        self.time_unit_dropdown = ttk.Combobox(root, textvariable=self.time_unit, values=["Hours", "Minutes", "Seconds"], state="readonly", width=47)
        self.time_unit_dropdown.grid(row=row, column=1, padx=4, pady=4)
        row += 1

        # Buttons
        ttk.Button(root, text="Save Profile", command=self.save_profile).grid(row=row, column=0, pady=10)
        ttk.Button(root, text="Launch Selected Profile", command=self.launch_profile).grid(row=row, column=1, pady=10)
        row += 1

        stop_btn = ttk.Button(root, text="Stop ZRPC", command=self.stop_rpc)
        stop_btn.grid(row=row, column=0, columnspan=2, pady=5)

    def load_profile_names(self):
        self.profile_names = [f.replace(".ini", "") for f in os.listdir(PROFILE_DIR) if f.endswith(".ini")]
        self.profile_menu['values'] = self.profile_names

    def load_profile(self, event=None):
        profile = self.current_profile.get()
        path = os.path.join(PROFILE_DIR, profile + ".ini")
        if not os.path.exists(path): return

        with open(path, "r") as f:
            lines = f.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].lower()
                continue
            if "=" in line and section:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                mapping = {
                    "ClientID": "client_id",
                    "Details": "details",
                    "State": "state",
                    "LargeImage": "large_image",
                    "LargeImageTooltip": "large_tooltip",
                    "SmallImage": "small_image",
                    "SmallImageTooltip": "small_tooltip"
                }
                if key in mapping:
                    entry_key = mapping[key]
                    self.entries[entry_key].delete(0, tk.END)
                    self.entries[entry_key].insert(0, val)

    def calculate_start_time(self):
        try:
            value = float(self.time_value_entry.get())
            unit = self.time_unit.get().lower()
            multiplier = {"hours": 3600, "minutes": 60, "seconds": 1}
            seconds_ago = value * multiplier.get(unit, 3600)
            now = int(time.time())
            return now - int(seconds_ago)
        except:
            return None

    def save_profile(self):
        start_time = self.calculate_start_time()

        profile_name = self.current_profile.get().strip()
        if not profile_name:
            messagebox.showerror("Error", "Enter/select a profile name.")
            return

        client_id = self.entries["client_id"].get().strip()
        large_image = self.entries["large_image"].get().strip()

        if not client_id or not large_image:
            messagebox.showerror("Error", "ClientID and LargeImage are required!")
            return

        path = os.path.join(PROFILE_DIR, profile_name + ".ini")

        with open(path, "w") as f:
            f.write("[Identifiers]\n")
            f.write(f"ClientID={client_id}\n\n")

            f.write("[State]\n")
            f.write(f"Details={self.entries['details'].get().strip()}\n")
            f.write(f"State={self.entries['state'].get().strip()}\n")
            f.write(f"StartTimestamp={start_time or ''}\n\n")

            f.write("[Images]\n")
            f.write(f"LargeImage={large_image}\n")
            f.write(f"LargeImageTooltip={self.entries['large_tooltip'].get().strip()}\n")
            f.write(f"SmallImage={self.entries['small_image'].get().strip()}\n")
            f.write(f"SmallImageTooltip={self.entries['small_tooltip'].get().strip()}\n")

        messagebox.showinfo("Saved", f"Profile '{profile_name}' saved.")
        self.load_profile_names()

    def launch_profile(self):
        start_time = self.calculate_start_time()

        if self.rpc:
            self.rpc.clear()
            self.rpc.close()

        client_id = self.entries["client_id"].get().strip()
        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()

            self.rpc.update(
                details=self.entries["details"].get().strip() or None,
                state=self.entries["state"].get().strip() or None,
                start=start_time,
                end=None,
                large_image=self.entries["large_image"].get().strip(),
                large_text=self.entries["large_tooltip"].get().strip() or None,
                small_image=self.entries["small_image"].get().strip() or None,
                small_text=self.entries["small_tooltip"].get().strip() or None
            )
            messagebox.showinfo("ZRPC Running", "Presence launched successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch presence:\n{e}")

    def stop_rpc(self):
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
                self.rpc = None
                messagebox.showinfo("ZRPC Stopped", "Presence cleared.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop presence:\n{e}")
        else:
            messagebox.showinfo("ZRPC Not Running", "No active Rich Presence to stop.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZRPCApp(root)
    root.mainloop()
