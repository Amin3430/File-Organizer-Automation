import os, threading, time, shutil, json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from organizer import categorize_and_move
from scanner import heuristic_scan
from mailer import send_report
from utils import now_str, read_json, write_json, ensure_folder

def main():
    BASE = os.path.dirname(__file__)
    ensure_folder(os.path.join(BASE, "trash"))

    # ---------- GUI setup ----------
    root = tk.Tk()
    root.title("File Organizer Automation")
    root.geometry("880x600")
    style = ttk.Style(root)
    current_theme = tk.StringVar(value="light")

    def apply_theme():
        t = current_theme.get()
        if t == "dark":
            bg, fg, accent = "#1e1e1e", "#ffffff", "#4cafef"
        else:
            bg, fg, accent = "#f0f0f0", "#000000", "#1976d2"

        root.configure(bg=bg)
        style.theme_use("clam")
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 11))
        style.configure("TRadiobutton", background=bg, foreground=fg, font=("Segoe UI", 10))

    apply_theme()

    # ---------- Variables ----------
    src_folder = tk.StringVar()
    dest_folder = tk.StringVar()
    status = tk.StringVar(value="Ready")

    # ---------- Helper for stylish buttons ----------
    def create_styled_button(parent, text, bg, fg="white", active_bg=None, command=None):
        active_bg = active_bg or bg
        btn = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 11, "bold"),
            activebackground=active_bg,
            activeforeground=fg,
            bd=0,
            relief="flat",
            padx=12,
            pady=6,
            highlightthickness=0,
            cursor="hand2",
            command=command
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=active_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ---------- Header ----------
    header = ttk.Frame(root, padding=12)
    header.pack(fill="x")
    ttk.Label(header, text="📂 File Organizer", font=("Segoe UI", 20, "bold")).pack(side="left")
    ttk.Label(header, textvariable=status, font=("Segoe UI", 10, "italic")).pack(side="right")

    # ---------- Body ----------
    body = ttk.Frame(root, padding=12)
    body.pack(fill="both", expand=True)

    # Source folder
    sf = ttk.Frame(body)
    sf.pack(fill="x", pady=6)
    ttk.Label(sf, text="Source Folder:").pack(side="left")
    ttk.Entry(sf, textvariable=src_folder, width=60, font=("Consolas", 10)).pack(side="left", padx=6)
    tk.Button(sf, text="Browse", command=lambda: src_folder.set(filedialog.askdirectory())).pack(side="left")

    # Destination folder
    df = ttk.Frame(body)
    df.pack(fill="x", pady=6)
    ttk.Label(df, text="Destination Folder:").pack(side="left")
    ttk.Entry(df, textvariable=dest_folder, width=56, font=("Consolas", 10)).pack(side="left", padx=6)
    tk.Button(df, text="Browse", command=lambda: dest_folder.set(filedialog.askdirectory())).pack(side="left")

    # ---------- Logging ----------
    def log(msg):
        t = now_str()
        with open(os.path.join(BASE, "gui.log"), "a", encoding="utf-8") as f:
            f.write(f"{t} - {msg}\n")
        status.set(msg)

    # ---------- Actions ----------
    actions = ttk.Frame(body)
    actions.pack(fill="x", pady=10)

    def do_organize():
        s, d = src_folder.get().strip(), dest_folder.get().strip()
        if not s or not d:
            messagebox.showwarning("Missing", "Choose source and destination folders")
            return

        def job():
            log("Organizing...")
            moved = categorize_and_move(s, d)
            if moved:
                write_json(os.path.join(BASE, "last_op.json"), {"moved": moved})
                log(f"Moved {len(moved)} files ✅")
            else:
                log("No files moved")

        threading.Thread(target=job, daemon=True).start()

    def do_undo():
        path = os.path.join(BASE, "last_op.json")
        if not os.path.exists(path):
            messagebox.showinfo("Undo", "No operation to undo")
            return

        data = read_json(path)
        moved = data.get("moved", [])
        failed = 0
        for src, dest in reversed(moved):
            try:
                if os.path.exists(dest):
                    ensure_folder(os.path.dirname(src))
                    shutil.move(dest, src)
            except:
                failed += 1

        if failed == 0:
            log("Undo completed 🔄")
            os.remove(path)
        else:
            log(f"Undo completed with {failed} failures ❌")

    def do_scan():
        folder = src_folder.get().strip()
        if not folder:
            messagebox.showwarning("Missing", "Choose a source folder to scan")
            return

        def job():
            log("Scanning...")
            findings = heuristic_scan(folder)
            if findings:
                report = "\n".join([f"{f['path']} -- {f['reason']}" for f in findings])
                messagebox.showwarning("Scan Results", f"Found {len(findings)} suspicious items.\n\n{report}")
                log(f"Scan complete: {len(findings)} findings ⚠️")
            else:
                messagebox.showinfo("Scan Results", "No suspicious files found")
                log("Scan complete: no findings ✅")

        threading.Thread(target=job, daemon=True).start()

    # Action buttons
    btn_organize = create_styled_button(actions, "Organize", "#43a047", "#ffffff", "#2e7d32", do_organize)
    btn_organize.pack(side="left", padx=8)
    btn_scan = create_styled_button(actions, "Scan Folder", "#fb8c00", "#ffffff", "#ef6c00", do_scan)
    btn_scan.pack(side="left", padx=8)
    btn_undo = create_styled_button(actions, "Undo Last", "#e53935", "#ffffff", "#c62828", do_undo)
    btn_undo.pack(side="left", padx=8)

    # ---------- Email Reminder ----------
    mr = ttk.Frame(body)
    mr.pack(fill="x", pady=10)
    ttk.Label(mr, text="Email Reminder (seconds):").pack(side="left")
    seconds_var = tk.IntVar(value=0)
    ttk.Entry(mr, textvariable=seconds_var, width=6, font=("Consolas", 10)).pack(side="left", padx=6)

    def schedule_mail():
        secs = seconds_var.get()
        if secs <= 0:
            messagebox.showwarning("Schedule", "Enter seconds > 0")
            return

        def job():
            time.sleep(secs)
            try:
                subject = "Daily File Organizer Report"
                body = f"""
Hello,

Your file organizer has completed its task at.
You can check the logs for details of files moved or scanned.

Best regards,
File Organizer Automation
"""
                send_report(subject, body)
                log("Email sent 📧")
                messagebox.showinfo("Email Sent", "Reminder email sent successfully!")
            except Exception as e:
                log(f"Email failed: {e}")
                messagebox.showerror("Email Failed", f"Could not send email:\n{e}")

        threading.Thread(target=job, daemon=True).start()
        log(f"Email scheduled in {secs} seconds ⏰")

    def test_email():
        try:
            send_report("Test Email - File Organizer", "This is a test email to verify App Password works.")
            log("Test email sent 📧")
            messagebox.showinfo("Email Test", "Test email sent successfully!")
        except Exception as e:
            log(f"Test email failed: {e}")
            messagebox.showerror("Email Test Failed", f"Could not send test email:\n{e}")

    btn_schedule = create_styled_button(mr, "Schedule Email", "#1e88e5", "#ffffff", "#1565c0", schedule_mail)
    btn_schedule.pack(side="left", padx=8)
    btn_test_email = create_styled_button(mr, "Test Email", "#1e88e5", "#ffffff", "#1565c0", test_email)
    btn_test_email.pack(side="left", padx=8)

    # ---------- Theme Toggle ----------
    theme_frame = ttk.Frame(body)
    theme_frame.pack(fill="x", pady=10)
    ttk.Radiobutton(theme_frame, text="Light Mode ☀️",
                    variable=current_theme, value="light", command=apply_theme).pack(side="left")
    ttk.Radiobutton(theme_frame, text="Dark Mode 🌙",
                    variable=current_theme, value="dark", command=apply_theme).pack(side="left")

    # ---------- Logs ----------
    logs = ttk.LabelFrame(body, text="Logs", padding=8)
    logs.pack(fill="both", expand=True, pady=8)
    log_box = tk.Text(logs, height=12, font=("Consolas", 10))
    log_box.pack(fill="both", expand=True)

    def refresh_logs():
        p = os.path.join(BASE, "gui.log")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                txt = f.read()
            log_box.delete("1.0", "end")
            log_box.insert("1.0", txt)
        root.after(3000, refresh_logs)

    refresh_logs()

    # ---------- Footer ----------
    footer = ttk.Frame(root, padding=8)
    footer.pack(fill="x", side="bottom")
    dt_label = ttk.Label(footer, text=now_str(), font=("Segoe UI", 10, "italic"))
    dt_label.pack(side="left")

    def tick():
        dt_label.config(text=now_str())
        root.after(1000, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
