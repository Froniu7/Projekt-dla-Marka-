import serial
import time

# --- KONFIGURACJA PORTU UART ---
PORT = 'COM5'           # <-- ZMIEŃ na swój port COM (np. COM4, COM5 itd.)
BAUDRATE = 9600         # prędkość transmisji
TIMEOUT = 1             # czas oczekiwania na odpowiedź w sekundach

# --- OTWARCIE PORTU ---
def open_serial():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        print(f"✅ Połączono z {PORT} ({BAUDRATE} bps)")
        return ser
    except serial.SerialException as e:
        print(f"❌ Błąd otwarcia portu: {e}")
        return None

# --- WYSYŁANIE KOMENDY ---
def send_command(ser, command):
    if not ser:
        print("⚠️ Port nie jest otwarty.")
        return
    ser.write((command + '\r\n').encode())  # CR+LF na końcu
    print(f"➡️ Wysłano: {command}")

# --- ODBIÓR ODPOWIEDZI ---
def read_response(ser):
    if not ser:
        return None
    time.sleep(0.1)  # chwila na odpowiedź
    response = ser.read_all().decode(errors='ignore').strip()
    if response:
        print(f"⬅️ Otrzymano: {response}")
    return response

# --- GŁÓWNY PROGRAM ---
if __name__ == "__main__":
    ser = open_serial()
    if not ser:
        input("Naciśnij Enter, aby zakończyć...")
        exit()

    print("💡 Wpisz komendę do wysłania (lub 'exit' aby zakończyć):")

    while True:
        cmd = input("> ")
        if cmd.lower() == 'exit':
            break
        send_command(ser, cmd)
        read_response(ser)

    ser.close()
    print("🔌 Połączenie zakończone.")
