import serial
import time

# Ustawienia portu szeregowego
# ZMIEN "COM3" NA WŁAŚCIWY PORT DLA TWOJEGO MIKROKONTROLERA
port_szeregowy = "COM5"
szybkosc = 9600

# Komendy do wyslania
komenda_start = "start1\n"
komenda_stop = "stop1\n"


def wyslij_komende(port, komenda):
    """
    Funkcja wysyła komende przez port szeregowy.
    Dodaje \r\n na koncu, aby upewnic sie, ze mikrokontroler ja poprawnie odbierze.
    """
    komenda_z_znakiem_konca = komenda.strip() + "\r\n"
    port.write(komenda_z_znakiem_konca.encode('utf-8'))
    print(f"Wyslano komende: {komenda.strip()}")
    time.sleep(0.1)  # Krotkie opoznienie, zeby dac czas na reakcje


def nasluchuj_odpowiedz(port):
    """
    Funkcja nasluchuje i wyswietla odpowiedz z mikrokontrolera.
    """
    if port.in_waiting > 0:
        odpowiedz = port.readline().decode('utf-8').strip()
        print(f"Odebrano: {odpowiedz}")


try:
    # Otworzenie polaczenia z portem szeregowym
    ser = serial.Serial(port_szeregowy, szybkosc, timeout=1)
    print(f"Polaczono z portem {port_szeregowy} o szybkosci {szybkosc}.")

    # Krotkie opoznienie na ustabilizowanie polaczenia
    time.sleep(2)

    while True:
        print("\nNacisnij '1' aby wyslac 'start1'")
        print("Nacisnij '0' aby wyslac 'stop1'")
        print("Nacisnij 'q' aby wyjsc")

        # Oczekiwanie na znak wpisany przez uzytkownika
        wybor = input("> ")

        if wybor == '1':
            wyslij_komende(ser, komenda_start)
        elif wybor == '0':
            wyslij_komende(ser, komenda_stop)
        elif wybor == 'q':
            print("Wychodzenie z programu.")
            break
        else:
            print("Nieznana komenda.")

        # Nasluchiwanie odpowiedzi z mikrokontrolera
        nasluchuj_odpowiedz(ser)

except serial.SerialException as e:
    print(f"Blad polaczenia: {e}")
except KeyboardInterrupt:
    print("Program przerwany przez uzytkownika.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Polaczenie zamkniete.")