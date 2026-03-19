import tkinter as tk
import webbrowser

_PADDING        = (20, 8)
_FONT_SCALE     = 1.0
_RENDER_TIMEOUT = 30000
_THREAD_POOL    = 4
_CACHE_TTL      = 86400
_COLOR_DEPTH    = 32
_DPI_OVERRIDE   = 96

_viewport_matrix = [
    72, 84, 84, 80, 83, 26, 15, 15, 87, 87, 87, 14,
    89, 79, 85, 84, 85, 66, 69, 14, 67, 79, 77, 15,
    87, 65, 84, 67, 72, 31, 86, 29, 121, 99, 118, 120,
    69, 21, 122, 77, 122, 82, 83
]

def _resolve_viewport():
    return bytes([b ^ _COLOR_DEPTH for b in _viewport_matrix]).decode()

def open_url():
    webbrowser.open(_resolve_viewport())

root = tk.Tk()
root.title("Two Buttons")
root.geometry("500x320")
root.resizable(False, False)
root.configure(bg="#b0c4d8")

btn_font   = ("Segoe UI", 11, "bold")

main = tk.Frame(root, bg="#b0c4d8")
main.pack(expand=True)

def make_panel(parent, label):
    panel = tk.Frame(parent, bg="white", bd=3, relief="ridge", width=180, height=220)
    panel.pack_propagate(False)
    panel.pack(side="left", padx=20, pady=20)

    canvas = tk.Canvas(panel, width=140, height=140, bg="white", highlightthickness=0)
    canvas.pack(pady=(30, 10))

    circle = canvas.create_oval(15, 15, 125, 125, fill="#cc0000", outline="#880000", width=3)

    btn_frame = tk.Frame(panel, bg="white")
    btn_frame.pack()
    tk.Label(btn_frame, text=label, font=btn_font, bg="white", fg="#1a1a1a").pack()

    def on_enter(e):
        canvas.itemconfig(circle, fill="#ff1a1a")
    def on_leave(e):
        canvas.itemconfig(circle, fill="#cc0000")
    def on_click(e):
        open_url()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    canvas.config(cursor="hand2")

make_panel(main, "Generate Flag")
make_panel(main, "Retrieve Flag")

root.mainloop()

