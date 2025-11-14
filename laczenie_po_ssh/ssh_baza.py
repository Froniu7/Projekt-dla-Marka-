import psycopg2
import sshtunnel
import json
import sys
import os
import paramiko

CONFIG_FILE = "config_WAN.json"
LOCAL_PORT = 5432 # Port na PC

def run_db_query_via_tunnel():
    # ---- Wczytanie konfiguracji ----
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Błąd wczytywania configu: {e}")
        sys.exit(1)

    ssh_conn = config["connection"]
    ssh_auth = config["auth"]
    db_cfg = config["database"]

    HOST = ssh_conn["host"]
    PORT = ssh_conn["port"]
    USERNAME = ssh_conn["username"]
    KEY_PATH = ssh_auth["key_path"]
    PASSPHRASE = ssh_auth.get("passphrase") or None

    DB_HOST = db_cfg["db_host"]
    DB_PORT = db_cfg["db_port"]
    DB_NAME = db_cfg["db_name"]
    DB_USER = db_cfg["db_user"]
    DB_PASS = db_cfg["db_password"]

    # ---- Ładowanie klucza (NIE ZMIENIAMY TEGO BLOKU) ----
    try:
        # Twój sprawdzony sposób ładowania klucza
        pkey = paramiko.RSAKey.from_private_key_file(KEY_PATH, password=PASSPHRASE)
        print("🔑 Klucz RSA załadowany.")
    except Exception as e:
        print(f"❌ Błąd ładowania klucza RSA: {e}")
        sys.exit(1)

    # ---- Ręczne tworzenie sesji SSH (JAK W TWOIM DZIAŁAJĄCYM KODZIE) ----
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"🌐 Łączenie SSH → {USERNAME}@{HOST}:{PORT}")
        ssh_client.connect(
            hostname=HOST,
            port=PORT,
            username=USERNAME,
            pkey=pkey,
            allow_agent=False,
            look_for_keys=False,
            timeout=10
        )
        print("✅ Połączenie SSH OK.")
    except Exception as e:
        print(f"❌ Błąd połączenia SSH: {e}")
        sys.exit(1)

    # ---- Utworzenie tunelu NA ISTNIEJĄCEJ SESJI SSH ----
    try:
        # KLUCZOWA ZMIANA: Używamy SSHTunnelForwarder i ręcznie przekazujemy klienta.
        # Jest to jedyny sposób na użycie istniejącej sesji bez błędu DSSKey,
        # który pojawia się podczas wewnętrznego łączenia sshtunnel.
        tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=(HOST, PORT), # Używamy tych danych, ale tunnel będzie używał klienta
            ssh_username=USERNAME,
            ssh_pkey=pkey,
            remote_bind_address=(DB_HOST, DB_PORT),
            local_bind_address=('127.0.0.1', LOCAL_PORT),
            # WŁĄCZENIE TRYBU KLIENTA I PRZEKAZANIE OBIEKTU SSHCLIENT
            ssh_forward_host='127.0.0.1', # Użyj tunelu do połączenia lokalnego
            ssh_forward_port=2222,         # Domyślny port SSH (opcjonalne, ale bezpieczne)
            client_mode=True,            # Mówimy, że używamy istniejącego klienta
        )
        # Przypisanie klienta do tunelu po jego utworzeniu
        tunnel.ssh_client = ssh_client

        # Rozpoczęcie tunelowania
        tunnel.start()

        print(f"🚇 Tunel działa: 127.0.0.1:{LOCAL_PORT} → {DB_HOST}:{DB_PORT}")

        # ---- Połączenie z PostgreSQL ----
        try:
            conn = psycopg2.connect(
                host="127.0.0.1",
                port=LOCAL_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
            )
            conn.close()
            print("🎉 Połączenie z bazą działa!")
        except Exception as e:
            print(f"❌ Błąd PostgreSQL: {e}")

    except Exception as e:
        print(f"❌ Błąd tunelowania: {e}")

    finally:
        # Zamykamy tunel, a następnie klienta SSH
        if 'tunnel' in locals() and tunnel.is_active:
            tunnel.stop()
        ssh_client.close()
        print("🔚 Zamknięto SSH i tunel.")


if __name__ == "__main__":
    run_db_query_via_tunnel()