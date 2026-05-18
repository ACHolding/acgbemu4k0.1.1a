# acgbemu4k0.1.py
# Python 3.14

import tkinter as tk
from tkinter import filedialog, messagebox
from pyboy import PyBoy

APP_TITLE = "acgbemu4k0.1"

BG = "#2b2b2b"
PANEL = "#3a3a3a"
SCREEN = "#111111"
BORDER = "#555555"
BTN_BG = "#1f1f1f"
TEXT = "#4aa3ff"


class ACGBEmu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("720x520")
        self.root.configure(bg=BG)

        self.rom_path = None

        self.make_menu()
        self.make_toolbar()
        self.make_screen()
        self.make_statusbar()

    def make_menu(self):
        menubar = tk.Menu(self.root, bg=PANEL, fg=TEXT)

        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        file_menu.add_command(label="Load ROM...", command=self.load_rom)
        file_menu.add_command(label="Start", command=self.start_emulator)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        emu_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        emu_menu.add_command(label="Reset")
        emu_menu.add_command(label="Pause")
        emu_menu.add_command(label="Save State")
        emu_menu.add_command(label="Load State")

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Emulation", menu=emu_menu)
        menubar.add_cascade(label="Tools")
        menubar.add_cascade(label="Help")

        self.root.config(menu=menubar)

    def make_toolbar(self):
        bar = tk.Frame(self.root, bg=PANEL, height=44)
        bar.pack(fill="x")

        buttons = [
            ("Open", self.load_rom),
            ("Start", self.start_emulator),
            ("Pause", None),
            ("Reset", None),
            ("Save", None),
            ("Load", None),
        ]

        for label, cmd in buttons:
            tk.Button(
                bar,
                text=label,
                command=cmd,
                bg=BTN_BG,
                fg=TEXT,
                activebackground="#000000",
                activeforeground=TEXT,
                relief="flat",
                padx=14,
                pady=6
            ).pack(side="left", padx=4, pady=6)

    def make_screen(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(expand=True, fill="both", padx=18, pady=18)

        frame = tk.Frame(
            outer,
            bg=BORDER,
            bd=0,
            relief="flat"
        )
        frame.pack(expand=True)

        self.screen = tk.Canvas(
            frame,
            width=480,
            height=432,
            bg=SCREEN,
            highlightthickness=3,
            highlightbackground=BORDER
        )
        self.screen.pack(padx=10, pady=10)

        self.screen.create_text(
            240,
            190,
            text=APP_TITLE,
            fill=TEXT,
            font=("Consolas", 26, "bold")
        )

        self.screen.create_text(
            240,
            230,
            text="Load a Game Boy ROM",
            fill="#9ccfff",
            font=("Consolas", 14)
        )

    def make_statusbar(self):
        self.status = tk.Label(
            self.root,
            text="Ready",
            bg=PANEL,
            fg=TEXT,
            anchor="w",
            font=("Consolas", 10),
            padx=8
        )
        self.status.pack(side="bottom", fill="x")

    def load_rom(self):
        path = filedialog.askopenfilename(
            title="Select Game Boy ROM",
            filetypes=[
                ("Game Boy ROMs", "*.gb *.gbc"),
                ("All files", "*.*")
            ]
        )

        if path:
            self.rom_path = path
            name = path.split("/")[-1]
            self.status.config(text=f"Loaded ROM: {name}")

    def start_emulator(self):
        if not self.rom_path:
            messagebox.showerror(APP_TITLE, "Load a ROM first.")
            return

        self.root.destroy()

        pyboy = PyBoy(
            self.rom_path,
            window="SDL2",
            window_title=APP_TITLE
        )
        pyboy.set_emulation_speed(1)  # real-time (~60 fps)

        while pyboy.tick():
            pass

        pyboy.stop()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ACGBEmu().run()
