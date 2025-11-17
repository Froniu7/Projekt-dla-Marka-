import os

# 🔹 Ścieżka do katalogu jako zmienna
directory_path = r"C:\Users\Marcin\.ssh"

# 🔹 Sprawdzenie, czy katalog istnieje
if not os.path.exists(directory_path):
    print(f"❌ Katalog nie istnieje: {directory_path}")
else:
    print(f"📂 Zawartość katalogu: {directory_path}\n")

    # 🔹 Lista plików i folderów
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            print(f"📄 Plik: {entry}")
        elif os.path.isdir(full_path):
            print(f"📁 Folder: {entry}")
