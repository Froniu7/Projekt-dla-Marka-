import json
import os
import sys
import psycopg2
from sshtunnel import SSHTunnelForwarder
import paramiko  # Wymagane do załadowania klucza

CONFIG_FILE = "config_WAN.json"


def run_db_via_tunnel():
    # ---- Wczytanie konfiguracji JSON ----
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Błąd wczytywania configu: {e}")
        sys.exit(1)

    # ---- Dane SSH ----
    ssh_cfg = config["connection"]
    ssh_auth = config["auth"]

    ssh_host = ssh_cfg["host"]
    ssh_port = ssh_cfg["port"]
    ssh_user = ssh_cfg["username"]

    key_path = ssh_auth["key_path"]
    passphrase = ssh_auth.get("passphrase") or None


    if not os.path.exists(key_path):

        print(f"❌ Błąd: nie znaleziono klucza SSH pod ścieżką: {key_path}")
        sys.exit(1)

    # 1. 🔑 RĘCZNE ŁADOWANIE KLUCZA JAKO OBIEKT PARAMIKO
    # To jest JEDYNY sposób, aby zatrzymać szukanie klucza id_rsa w Twojej konfiguracji bibliotek.
    try:
        pkey = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
        print("🔑 Klucz SSH załadowany jako obiekt, pomijam szukanie systemowe.")
    except Exception as e:
        print(f"❌ Błąd ładowania klucza RSA: {e}")
        sys.exit(1)

    # ---- Dane PostgreSQL ----
    db_cfg = config["database"]
    db_host_json = db_cfg.get("db_host", "127.0.0.1")
    db_port = db_cfg.get("db_port", 5432)
    db_name = db_cfg["db_name"]
    db_user = db_cfg["db_user"]
    db_pass = db_cfg["db_password"]
    ssh_port_lan = db_cfg.get("ssh_port_lan")

    # ➡️ Używamy 127.0.0.1 jako docelowego hosta w tunelu ⬅️
    TARGET_DB_HOST = '127.0.0.1'
    LOCAL_TUNNEL_PORT = 6543

    print(f"Dane sieciowe: WAN Port {ssh_port}, LAN Port SSH {ssh_port_lan}")

    # ---- Utworzenie tunelu SSH ----
    try:
        with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                # KLUCZOWA ZMIANA: Przekazujemy załadowany OBIEKT klucza pkey
                ssh_pkey=pkey,
                # Argument ssh_private_key_password staje się zbędny
                remote_bind_address=(TARGET_DB_HOST, db_port),
                local_bind_address=('127.0.0.1', LOCAL_TUNNEL_PORT)
        ) as tunnel:

            print(f"✅ Tunel SSH aktywny: 127.0.0.1:{tunnel.local_bind_port} → {TARGET_DB_HOST}:{db_port}")

            # ---- Połączenie z PostgreSQL przez tunel ----
            try:
                conn = psycopg2.connect(
                    host="127.0.0.1",
                    port=tunnel.local_bind_port,
                    database=db_name,
                    user=db_user,
                    password=db_pass,
                    connect_timeout=5
                )

                # Przykładowe zapytanie
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                print("🎉 Połączenie z bazą działa! Wersja PostgreSQL:", cursor.fetchone()[0])

                conn.close()
                print("🎉 Połączenie z bazą PostgreSQL zakończone poprawnie!")
            except Exception as e:
                print(f"❌ Błąd połączenia z PostgreSQL: {e}")

    except Exception as e:
        print(f"❌ Błąd tunelowania SSH: {e}")


if __name__ == "__main__":
    run_db_via_tunnel()