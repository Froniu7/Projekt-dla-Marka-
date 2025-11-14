import os
import sys
import subprocess

def get_program_dir():
    if getattr(sys, 'frozen', False):
        # jeśli uruchomione jako .exe (np. PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # jeśli jako zwykły skrypt .py
        return os.path.dirname(os.path.abspath(__file__))

def main(plik):
    program_dir = get_program_dir()
    target = os.path.join(program_dir, plik)

    # zmień katalog roboczy na katalog programu
    os.chdir(program_dir)
    print(f"Uruchamiam {target} w katalogu {program_dir}")

    # uruchom właściwy program
    subprocess.Popen([target], cwd=program_dir)

if __name__ == "__main__":
    main("generowanie_schematy_SVC.exe")
