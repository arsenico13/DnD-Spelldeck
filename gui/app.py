from pathlib import Path
import sys
import tkinter as tk

# When launched as `python3 gui/app.py`, Python adds `gui/` to `sys.path`
# instead of the repository root. Insert the parent directory explicitly so
# `gui.*` and `spelldeck.*` imports work in the direct-script workflow.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gui.main_window import SpellDeckMainWindow


def main():
    root = tk.Tk()
    root.title("D&D Spelldeck - Magie")
    root.minsize(760, 520)
    SpellDeckMainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
