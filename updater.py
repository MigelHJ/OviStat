import json
import os
import shutil
import subprocess
import sys
from tkinter import messagebox
import urllib.request
import zipfile

# ÁLLÍTSD BE A SAJÁT ADATAIDAT:
GITHUB_USER = "MigelHJ"  # Pl. vorak...
GITHUB_REPO = "OviStat"
CURRENT_VERSION = "v0.5.7"  # Mindig növeld új kiadásnál (v1.0.1, v1.0.2...)


def get_latest_release():
  """Lekéri a legfrissebb Release adatait a GitHub REST API-ról."""
  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
  req = urllib.request.Request(url, headers={"User-Agent": "OviStat-Updater"})
  with urllib.request.urlopen(req, timeout=10) as response:
    return json.loads(response.read().decode())


def get_app_dir():
  """Visszaadja a program valós mappáját (.exe és sima Python esetén is)."""
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  return os.path.dirname(os.path.abspath(__file__))


def run_update(parent_window):
  try:
    data = get_latest_release()
    latest_tag = data.get("tag_name", "")

    # Verzió összehasonlítás
    if latest_tag == CURRENT_VERSION or not latest_tag:
      messagebox.showinfo(
          "Frissítés",
          f"A program naprakész! Jelenlegi verzió: {CURRENT_VERSION}",
          parent=parent_window,
      )
      return

    confirm = messagebox.askyesno(
        "Új verzió elérhető!",
        f"Elérhető egy új verzió: {latest_tag}\nJelenlegi: {CURRENT_VERSION}\n\n"
        "Szeretnéd most frissíteni az alkalmazást?\n(A mentett gyerek adatok megmaradnak!)",
        parent=parent_window,
    )
    if not confirm:
      return

    # Megkeressük az 'OviStat.zip' csomagot a release-ben
    assets = data.get("assets", [])
    download_url = None
    for asset in assets:
      if asset["name"].endswith(".zip"):
        download_url = asset["browser_download_url"]
        break

    if not download_url:
      messagebox.showerror(
          "Hiba",
          "Nem található letölthető ZIP fájl a legújabb kiadásban!",
          parent=parent_window,
      )
      return

    app_dir = get_app_dir()
    temp_zip = os.path.join(app_dir, "update_temp.zip")
    extract_folder = os.path.join(app_dir, "update_temp_extracted")

    # 1. Letöltés
    urllib.request.urlretrieve(download_url, temp_zip)

    # 2. Kicsomagolás temp mappába
    if os.path.exists(extract_folder):
      shutil.rmtree(extract_folder)
    with zipfile.ZipFile(temp_zip, "r") as zip_ref:
      zip_ref.extractall(extract_folder)

    # Ha a ZIP belsejében egyetlen fő mappa van (pl. OviStat), lépjünk be abba
    source_dir = extract_folder
    items = os.listdir(extract_folder)
    if len(items) == 1 and os.path.isdir(
        os.path.join(extract_folder, items[0])
    ):
      source_dir = os.path.join(extract_folder, items[0])

    # 3. Frissítő Batch script generálása
    # Ez megvárja, míg a most futó app bezárul, felülírja a fájlokat, de kihagyja a CSV-t!
    updater_bat = os.path.join(app_dir, "apply_update.bat")
    bat_content = f"""@echo off
        timeout /t 2 /nobreak > nul
        xcopy "{source_dir}" "{app_dir}" /E /Y /EXCLUDE:exclude.txt
        del "{temp_zip}"
        rd /s /q "{extract_folder}"
        start "" "{sys.executable}"
        del "%~f0"
        """
    # Kizárási lista készítése (a gyerek_adatok.csv véletlenül se íródjon felül)
    exclude_file = os.path.join(app_dir, "exclude.txt")
    with open(exclude_file, "w", encoding="utf-8") as ef:
      ef.write("gyerek_adatok.csv\n")

    with open(updater_bat, "w", encoding="utf-8") as bf:
      bf.write(bat_content)

    messagebox.showinfo(
        "Újraindítás",
        "A frissítés letöltve. Az alkalmazás most újraindul a frissítés érvényesítéséhez.",
        parent=parent_window,
    )

    # Batch fájl elindítása a háttérben, majd azonnali kilépés
    subprocess.Popen([updater_bat], shell=True)
    sys.exit(0)

  except Exception as e:
    messagebox.showerror(
        "Frissítési hiba", f"Hiba történt:\n{str(e)}", parent=parent_window
    )