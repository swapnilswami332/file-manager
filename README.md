# file-manager
Sorts file according to file extension. Option to move or copy.
A small Python desktop utility (Tkinter GUI) that organizes files in a folder into category subfolders based on file extensions, with an option to move or copy files. I inspected the README and the main modules (categories.py, file_sorter.py, gui.py, main.py) to produce this summary.

Stack
Language(s): Python (requires Python 3 — code uses modern typing like list[str], so Python 3.9+ is recommended)
Framework / runtime: Tkinter desktop GUI (no web framework)
Notable libraries: tkinter (UI), shutil (file copy/move), collections.Counter (summary counting) — all standard library
How it's organized
Code
README.md           short description and overview
main.py             program entry point (creates and runs GUI)
gui.py              Tkinter-based FileManagerApp (UI, preview, logs, status)
file_sorter.py      FileSorter class: preview(), sort(), safe_dest_path()
categories.py       CATEGORY_MAP, SKIP_FILES, get_category(filename)
How it fits together: main.py instantiates FileManagerApp (gui.py). The GUI uses FileSorter (file_sorter.py) to inspect and operate on the selected folder; FileSorter consults categories.py to map file extensions to category names, creates category folders, and moves or copies files while avoiding collisions with safe_dest_path.

How to run it
Ensure you have Python 3.9+ and tkinter installed (on many Linux systems: apt install python3-tk).
From a fresh clone, run the GUI:
Code
python3 main.py
There are no external dependencies or tests included. The app requires a desktop environment (X/Wayland) to display the Tk window.
Try asking
Can you add a CLI mode (argument parsing) so FileSorter can be run without the GUI (refer to main.py and file_sorter.py)?
Should categories be configurable via a JSON or YAML file instead of the hard-coded CATEGORY_MAP in categories.py?
Do you want recursive sorting of files inside subdirectories (file_sorter._list_files currently lists only top-level files)?
