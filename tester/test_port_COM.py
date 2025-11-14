import serial
import time
import sys
import struct
import math

# --- KONFIGURACJA PORTU ---
# Ustaw port COM, który ma być użyty (np. 'COM3', 'COM5', '3', '5')
PORT_COM = '5'
# --------------------------


# Walidacja i korekta nazwy portu
# Upewniamy się, że nazwa portu zaczyna się od 'COM'
COM = PORT_COM
if not COM.upper().startswith('COM'):
    COM = f'COM{COM}'
    print(f"Uwaga: Skorygowana nazwa portu: {COM}")

mikrokontroler = None

try:
    # otwarcie portu
    mikrokontroler = serial.Serial(COM, 9600, timeout=2)
    time.sleep(1)  # chwilka na stabilizację połączenia

    # Wysyłana komenda, która nie jest zdefiniowana w Arduino,
    # co spowoduje, że Arduino odeśle "Nieznana komenda".
    # Wymagany jest znak nowej linii (\n) na końcu, aby Arduino wiedziało, kiedy kończy się komenda.
    wiadomosc = "test\n"

    mikrokontroler.write(wiadomosc.encode('utf-8'))
    print(f"Wysłano: {wiadomosc.strip()}")

    # oczekiwanie na odpowiedź
    # Czytanie aż do znaku nowej linii lub do timeoutu.
    odpowiedz = mikrokontroler.readline().decode('utf-8').strip()

    if odpowiedz:
        # Oczekiwana odpowiedź od Arduino to "Nieznana komenda"
        print(f"Odpowiedź z mikrokontrolera: {odpowiedz}")
    else:
        print("Brak odpowiedzi (timeout).")

except serial.SerialException as e:
    # Wyświetlanie błędu (np. jeśli port jest zajęty lub nie istnieje).
    print(f"Błąd portu szeregowego: {e}")

finally:
    # Zamykanie portu, jeśli został poprawnie zainicjowany i jest otwarty
    if mikrokontroler is not None and mikrokontroler.is_open:
        mikrokontroler.close()
        print("Zamknięto port COM.")
