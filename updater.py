import json
import os
import shutil
import subprocess
import sys
from tkinter import messagebox
import urllib.request
import zipfile

GITHUB_USER = "MigelHJ"
GITHUB_REPO = "OviStat"
CURRENT_VERSION = "v0.6.0"  # A futó program aktuális verziója


def get_latest_release():
  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
  req = urllib.request.Request(url, headers={"User-Agent": "OviStat-Updater"})
  with urllib.request.urlopen(req, timeout=10) as response:
    return json.loads(response.read().decode())


def get_app_dir():
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  return os.path.dirname(os.path.abspath(__file__))


def run_update(parent_window):
  try:
    data = get_latest_release()
    latest_tag = data.get("tag_name", "")

    if latest_tag == CURRENT_VERSION or not latest_tag:
      messagebox.showinfo(
          "Frissítés",
          f"A program naprakész! Jelenlegi verzió: {CURRENT_VERSION}",
          parent=parent_window,
      )
      return

    confirm = messagebox.askyesno(
        "Új verzió elérhető!",
        f"Új verzió érhető el: {latest_tag}\nJelenlegi: {CURRENT_VERSION}\n\n"
        "Szeretnéd most frissíteni az alkalmazást?\n(A mentett adatok megmaradnak!)",
        parent=parent_window,
    )
    if not confirm:
      return

    assets = data.get("assets", [])
    download_url = None
    for asset in assets:
      if asset.get("name", "").lower().endswith(".zip"):
        download_url = asset["browser_download_url"]
        break

    if not download_url:
      messagebox.showerror(
          "Hiba",
          "Nem található letölthető ZIP fájl a kiadásban!",
          parent=parent_window,
      )
      return

    app_dir = get_app_dir()
    temp_zip = os.path.join(app_dir, "update_temp.zip")
    extract_folder = os.path.join(app_dir, "update_temp_extracted")

    # 1. Letöltés
    urllib.request.urlretrieve(download_url, temp_zip)

    # 2. Kicsomagolás
    if os.path.exists(extract_folder):
      shutil.rmtree(extract_folder, ignore_errors=True)

    with zipfile.ZipFile(temp_zip, "r") as zip_ref:
      zip_ref.extractall(extract_folder)

    # Megkeressük a valódi tartalmat (ha a ZIP-ben egy gyökérmappa volt)
    source_dir = extract_folder
    items = os.listdir(extract_folder)
    if len(items) == 1 and os.path.isdir(
        os.path.join(extract_folder, items[0])
    ):
      source_dir = os.path.join(extract_folder, items[0])

    # 3. Készítünk egy megbízható frissítő Batch fájlt
    updater_bat = os.path.join(app_dir, "apply_update.bat")
    pid = os.getpid()
    exe_name = os.path.basename(sys.executable)

    # Robocopy-t használunk: /E (almappák), /IS (felülírás), /XF (gyerek_adatok.csv kihagyása)
    bat_content = f"""@echo off
        chcp 65001 > nul
        echo Frissítés folyamatban, kérlek várj...

        :: Megvárjuk, hogy a régi folyamat leálljon, ha nem áll le, kilőjük
        taskkill /F /PID {pid} >nul 2>&1
        timeout /t 2 /nobreak > nul

        :: Fájlok átmásolása (a gyerek_adatok.csv és maga a bat fájl kihagyásával)
        robocopy "{source_dir}" "{app_dir}" /E /IS /IT /XF gyerek_adatok.csv apply_update.bat > nul

        :: Ideiglenes fájlok takarítása
        del /F /Q "{temp_zip}" > nul 2>&1
        rd /s /q "{extract_folder}" > nul 2>&1

        :: Program újraindítása
        start "" "{os.path.join(app_dir, exe_name)}"

        :: Önmagát törli a batch fájl
        del "%~f0"
        """

    with open(updater_bat, "w", encoding="utf-8") as bf:
      bf.write(bat_content)

    messagebox.showinfo(
        "Újraindítás",
        "A frissítés készen áll! Az alkalmazás most bezárul és frissíti magát.",
        parent=parent_window,
    )

    # Batch fájl futtatása független folyamatként
    subprocess.Popen(
        ["cmd.exe", "/c", updater_bat],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

    # 4. A CustomTkinter ablak és a teljes Python folyamat kényszerített bezárása
    try:
      parent_window.quit()
      parent_window.destroy()
    except Exception:
      pass

    os._exit(0)  # Azonnal kilövi a folyamatot, nem vár meg semmit

  except Exception as e:
    messagebox.showerror(
        "Frissítési hiba", f"Hiba történt:\n{str(e)}", parent=parent_window
    )