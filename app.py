import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import platform
import re

def start_arp():
    output_box.delete(1.0, tk.END)
    
    thread = threading.Thread(target=run_arp)
    thread.daemon = True
    thread.start()

def run_arp():
    system_os = platform.system()
    command = ["arp", "-a"]

    try:
        creation_flag = 0
        if system_os == "Windows":
            creation_flag = subprocess.CREATE_NO_WINDOW

        result = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=creation_flag
        )

        for line in iter(result.stdout.readline, ''):
            line_strip = line.strip()

            # Dacă linia conține "dynamic" → verde
            if re.search(r"\bdynamic\b", line_strip, re.IGNORECASE):
                output_box.insert(tk.END, line_strip + "\n", "dynamic")
            else:
                output_box.insert(tk.END, line_strip + "\n")

            output_box.see(tk.END)

    except Exception as e:
        output_box.insert(tk.END, f"Eroare: {e}\n", "fail")

# Interfață
root = tk.Tk()
root.title("ARP Tool by AdrianT 2025")
root.geometry("600x480")
root.resizable(False, False)  # 🚫 Blochează resize

# Buton Start ARP
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

arp_button = tk.Button(button_frame, text="Run ARP -a", font=("Arial", 12), command=start_arp)
arp_button.pack(side="left", padx=5)

# Consolă Output
output_box = scrolledtext.ScrolledText(root, width=70, height=20, font=("Consolas", 10))
output_box.tag_config("dynamic", foreground="green")  # culoare verde pentru dynamic
output_box.pack(pady=10)

# Copyright
copyright_label = tk.Label(root, text="© AdrianT", font=("Arial", 8), anchor="e")
copyright_label.pack(side="bottom", anchor="se", padx=5, pady=5)

root.mainloop()
