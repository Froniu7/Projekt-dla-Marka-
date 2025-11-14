import paramiko
import json
import os

# --- KONFIGURACJA STAŁYCH ---
config_file = 'config_WAN.json'
ALLOW_AGENT = False
LOOK_FOR_KEYS = False
# ----------------------------

# 1. Ustalanie katalogu, w którym znajduje się skrypt
# Pliki będą zapisywane w tym samym folderzea
LOCAL_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Wczytanie i parsowanie konfiguracji
try:
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Przyjmuję, że używasz już ustrukturyzowanego JSON-a:
    HOST = config['connection']['host']
    PORT = config['connection']['port']
    USERNAME = config['connection']['username']

    KEY_PATH = config['auth']['key_path']
    # Passphrase jest None, jeśli w JSON jest puste, co jest OK
    PASSPHRASE = config['auth']['passphrase'] if config['auth']['passphrase'] else None

    # Plik, który nas interesuje
    REMOTE_FILE_PATH = config['files']['remote_file']

except Exception as e:
    print(f"Błąd wczytywania konfiguracji: {e}")
    exit(1)

# Sprawdzenie ścieżki do klucza (jak poprzednio)
if not os.path.exists(KEY_PATH):
    print(f"Błąd: Klucz prywatny nie został znaleziony pod ścieżką: {KEY_PATH}")
    exit(1)


# --- Funkcja Pobierania SFTP ---

def download_file_sftp(ssh_client, remote_path, local_dir):
    """Pobiera plik za pomocą klienta SFTP do podanego katalogu."""
    sftp_client = None
    try:
        # 1. Ustal lokalną ścieżkę zapisu
        file_name = os.path.basename(remote_path)
        local_path = os.path.join(local_dir, file_name)

        print(f"\nRozpoczynam pobieranie pliku SFTP...")
        print(f"Plik zostanie zapisany jako: {local_path}")

        # 2. Otwarcie sesji SFTP
        sftp_client = ssh_client.open_sftp()

        # 3. Pobranie pliku
        sftp_client.get(remote_path, local_path)

        print(f"SUKCES: Plik '{file_name}' pobrano pomyślnie.")
        return True
    except Exception as e:
        print(f"BŁĄD SFTP: Nie udało się pobrać pliku. {e}")
        return False
    finally:
        if sftp_client:
            sftp_client.close()


# --- Główny Blok Logiki ---

ssh_client = None
try:
    # 3. Jawne załadowanie klucza (bezpieczna metoda)
    try:
        pkey = paramiko.RSAKey.from_private_key_file(KEY_PATH, password=PASSPHRASE)
    except Exception as e:
        print(f"Błąd ładowania klucza: {e}")
        exit(1)

    # 4. Inicjalizacja klienta SSH i połączenie
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=HOST,
        port=PORT,
        username=USERNAME,
        pkey=pkey,
        allow_agent=ALLOW_AGENT,
        look_for_keys=LOOK_FOR_KEYS,
        timeout=10
    )
    print(f"Połączenie SSH nawiązane pomyślnie z {USERNAME}@{HOST}:{PORT}.")

    # 5. Wykonanie zdalnego polecenia (CAT - jak poprzednio)
    REMOTE_COMMAND = f"cat {REMOTE_FILE_PATH}"
    print(f"\nWykonuję polecenie: '{REMOTE_COMMAND}' (Weryfikacja zawartości)")
    stdin, stdout, stderr = ssh_client.exec_command(REMOTE_COMMAND)

    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    exit_status = stdout.channel.recv_exit_status()

    print(f"\n--- Zawartość pliku (stdout) ---")
    if output:
        print(output)
    else:
        print("Brak danych na standardowym wyjściu.")

    # 6. POBIERANIE PLIKU ZA POMOCĄ SFTP
    download_file_sftp(ssh_client, REMOTE_FILE_PATH, LOCAL_PROJECT_DIR)


except paramiko.AuthenticationException:
    print("BŁĄD UWIEPRZYTELNIENIA: Serwer odrzucił klucz.")
except paramiko.SSHException as e:
    print(f"Błąd: Problem z połączeniem SSH lub wykonaniem polecenia: {e}")
except Exception as e:
    print(f"Wystąpił nieoczekiwany błąd: {e}")

finally:
    # 7. Zamknięcie połączenia
    if ssh_client:
        ssh_client.close()
        print("\nPołączenie SSH zamknięte.")