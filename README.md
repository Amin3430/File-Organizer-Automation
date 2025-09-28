# File Organizer Automation with GUI

Features:
- Organize files by extension into categorized folders
- Heuristic malware scanner (flags suspicious files, no destructive actions)
- Undo last move operation
- Logging with timestamped entries
- Date & time shown in GUI
- Dark and Light mode toggle
- Email reminder (SMTP-based) for reports
- Stylish Tkinter/ttk GUI with progress and logs

How to run:
1. Install requirements: `pip install -r requirements.txt`
2. Fill SMTP settings in `config.json`
3. Run: `python main.py`

This project is educational. The scanner uses heuristics and file extension checks only.
