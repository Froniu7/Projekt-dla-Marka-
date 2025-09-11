import serial
import time

# ustaw swój port (np. "COM3" na Windows albo "/dev/ttyUSB0" na Linux)
PORT = "COM5"
BAUDRATE = 9600

# otwarcie portu
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

time.sleep(2)  # chwilka na reset Arduino po otwarciu portu

try:
    while True:
        # wyślij '1'
        ser.write(b"1")

        # odbierz odpowiedź
        response = ser.readline().decode("utf-8").strip()

        if response:
            print("Odpowiedź Arduino:", response)

        time.sleep(1)  # wysyłaj co 1 sekundę
except KeyboardInterrupt:
    print("Zatrzymano")
finally:
    ser.close()
