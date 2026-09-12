import os
import subprocess
import sys
from tkinter import messagebox


def check_for_updates() -> bool:
  """Checks whether the remote branch has new commits."""
  try:
    subprocess.run(
        ["git", "fetch", "origin", "main"], check=True, capture_output=True
    )
    local_hash = (
        subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    )
    remote_hash = (
        subprocess.check_output(["git", "rev-parse", "origin/main"])
        .decode()
        .strip()
    )
    return local_hash != remote_hash
  except Exception:
    return False


def run_update(parent_window):
  """Pulls latest commits from GitHub while keeping data intact."""
  try:
    # 1. Check if an update is even available
    if not check_for_updates():
      messagebox.showinfo(
          "Frissítés",
          "A program már a legfrissebb verziót futtatja!",
          parent=parent_window,
      )
      return

    confirm = messagebox.askyesno(
        "Frissítés elérhető",
        "Új verzió érhető el a GitHubon!\n\nSzeretnéd most frissíteni a"
        " programot?\n(A mentett adatok és a gyerek_adatok.csv nem vesznek"
        " el.)",
        parent=parent_window,
    )
    if not confirm:
      return

    # 2. Safety stash for any modified local script files
    subprocess.run(["git", "stash"], check=False, capture_output=True)

    # 3. Pull latest code
    subprocess.run(
        ["git", "pull", "origin", "main"],
        check=True,
        capture_output=True,
        text=True,
    )

    # 4. Update pip dependencies if requirements.txt was modified
    if os.path.exists("requirements.txt"):
      subprocess.run(
          [
              sys.executable,
              "-m",
              "pip",
              "install",
              "-r",
              "requirements.txt",
              "--quiet",
          ],
          check=False,
          capture_output=True,
      )

    # 5. Restart prompt
    restart = messagebox.askyesno(
        "Sikeres frissítés",
        "A program sikeresen frissült!\n\nSzeretnéd most újraindítani az"
        " alkalmazást?",
        parent=parent_window,
    )
    if restart:
      os.execv(sys.executable, [sys.executable] + sys.argv)

  except subprocess.CalledProcessError as e:
    err_text = e.stderr if hasattr(e, "stderr") and e.stderr else str(e)
    messagebox.showerror(
        "Frissítési hiba",
        f"Nem sikerült a frissítés:\n{err_text}",
        parent=parent_window,
    )
  except Exception as e:
    messagebox.showerror(
        "Hiba", f"Váratlan hiba történt:\n{str(e)}", parent=parent_window
    )