import serial
import time

def test_mikrokontroler_bez_zamkniecia(COM):
    """
    Otwiera port COM, wysyła testową komendę i zwraca obiekt Serial.
    Port pozostaje otwarty.
    """
    try:
        mikrokontroler = serial.Serial(COM, 9600, timeout=2)
        time.sleep(1)  # chwilka na stabilizację połączenia

        # Wysłanie testowej wiadomości
        wiadomosc = "test\n"
        mikrokontroler.write(wiadomosc.encode('utf-8'))
        print(f"Wysłano: {wiadomosc.strip()}")

        # Odczyt odpowiedzi
        odpowiedz = mikrokontroler.readline().decode('utf-8').strip()
        if odpowiedz:
            print(f"Odpowiedź z mikrokontrolera: {odpowiedz}")
        else:
            print("Brak odpowiedzi (timeout).")

        return mikrokontroler, odpowiedz  # zwracamy obiekt Serial

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
        return None


def wyslij_komende(mikrokontroler, komenda):
    """
    Wysyła komendę do już otwartego portu mikrokontrolera
    i zwraca odpowiedź.
    """
    if mikrokontroler is None or not mikrokontroler.is_open:
        print("Port COM nie jest otwarty!")
        return None

    if not komenda.endswith('\n'):
        komenda += '\n'

    try:
        mikrokontroler.write(komenda.encode('utf-8'))
        print(f"Wysłano: {komenda.strip()}")

        odpowiedz = mikrokontroler.readline().decode('utf-8').strip()
        if odpowiedz:
            print(f"Odpowiedź z mikrokontrolera: {odpowiedz}")
            return odpowiedz
        else:
            print("Brak odpowiedzi (timeout).")
            return None

    except Exception as e:
        print(f"Błąd podczas wysyłania komendy: {e}")
        return None

def check_power_within_limits(expected_power, measured_power, upper_float, lower_float):
    """
    Sprawdza, czy zmierzona moc mieści się w widełkach, gdzie widełki podane są jako float:
    1% = 0.01

    :param expected_power: moc oczekiwana (float)
    :param measured_power: moc zmierzona (float)
    :param upper_float: górna granica w formie float (np. 0.01 = 1%)
    :param lower_float: dolna granica w formie float (np. 0.01 = 1%)
    :return: (True/False, str) - czy moc mieści się w widełkach, komunikat
    """
    lower_limit = expected_power * (1 - lower_float)
    upper_limit = expected_power * (1 + upper_float)

    if lower_limit <= measured_power <= upper_limit:
        return True, f"Moc zmierzona {measured_power:.3f} mieści się w widełkach ({lower_limit:.3f} - {upper_limit:.3f})"
    else:
        return False, f"Moc zmierzona {measured_power:.3f} NIE mieści się w widełkach ({lower_limit:.3f} - {upper_limit:.3f})"


def get_first_float_from_string(text):
    """
    Zwraca pierwszą wartość liczbową (float) ze stringa — od początku tekstu do pierwszej spacji.
    Przykład: "233.86582946777344 V" -> 233.86582946777344
    """
    try:
        first_part = text.strip().split(" ")[0]
        return float(first_part)
    except (ValueError, IndexError):
        return None  # jeśli nie uda się przekonwertować

def get_second_float_from_string(text):
    """
    Zwraca pierwszą wartość liczbową (float) ze stringa — od początku tekstu do pierwszej spacji.
    Przykład: "233.86582946777344 V" -> 233.86582946777344
    """
    try:
        first_part = text.strip().split(" ")[4]
        return float(first_part)
    except (ValueError, IndexError):
        return None  # jeśli nie uda się przekonwertować




def zapisz_wynik_testu_dziala(nazwa_pliku, rodzaj, moc, model, wynik_testu):
    import csv
    import os
    """
    Zapisuje dane testu do pliku CSV.
    Jeśli plik nie istnieje — tworzy go i dodaje nagłówek.
    Automatycznie nadaje numer podzespołu (kolejny numer wiersza).
    """
    plik_istnieje = os.path.exists(nazwa_pliku)
    numer = 1

    # Jeśli plik istnieje, odczytaj ostatni poprawny numer
    if plik_istnieje:
        with open(nazwa_pliku, mode='r', newline='', encoding='utf-8') as f:
            reader = [row for row in csv.reader(f) if row]  # usuń puste wiersze
            if len(reader) > 1:  # pierwszy to nagłówek
                last_row = reader[-1]
                try:
                    numer = int(last_row[0]) + 1
                except (ValueError, IndexError):
                    numer = 1

    # Otwórz plik w trybie dopisania
    with open(nazwa_pliku, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Jeśli plik nowy, dodaj nagłówki
        if not plik_istnieje:
            writer.writerow(["Nr", "Rodzaj", "Moc", "Model", "Wynik testu"])
        # Dopisz dane
        writer.writerow([numer, rodzaj, moc, model, wynik_testu])

    print(f"✅ Zapisano wiersz nr {numer} do pliku: {nazwa_pliku}")
    print("")
    print(f"          {wynik_testu}")
    print("")
    print(f"          {numer}")
    print("")

def zapisz_wynik_testu_niedziala(nazwa_pliku, rodzaj, moc, model, wynik_testu):
    import csv
    import os
    """
    Zapisuje dane testu do pliku CSV.
    Jeśli plik nie istnieje — tworzy go i dodaje nagłówek.
    Automatycznie nadaje numer podzespołu (kolejny numer wiersza).
    """
    plik_istnieje = os.path.exists(nazwa_pliku)
    numer = 1

    # Jeśli plik istnieje, odczytaj ostatni poprawny numer
    if plik_istnieje:
        with open(nazwa_pliku, mode='r', newline='', encoding='utf-8') as f:
            reader = [row for row in csv.reader(f) if row]  # usuń puste wiersze
            if len(reader) > 1:  # pierwszy to nagłówek
                last_row = reader[-1]
                try:
                    numer = int(last_row[0]) + 1
                except (ValueError, IndexError):
                    numer = 1

    # Otwórz plik w trybie dopisania
    with open(nazwa_pliku, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Jeśli plik nowy, dodaj nagłówki
        if not plik_istnieje:
            writer.writerow(["Nr", "Rodzaj", "Moc", "Model", "Wynik testu"])
        # Dopisz dane
        writer.writerow([numer, rodzaj, moc, model, wynik_testu])

    print(f"❌ Zapisano wiersz nr {numer} do pliku: {nazwa_pliku}")
    print("")
    print(f"          {wynik_testu}")
    print("")
    print(f"          {numer}")
    print("")

if __name__ == "__main__":
    # Otwieramy port i pobieramy obiekt Serial
    mikrokontroler, odpowiedz = test_mikrokontroler_bez_zamkniecia('COM5')

    # Wysyłamy komendy korzystając z tego samego obiektu
    if mikrokontroler:
        wyslij_komende(mikrokontroler, "test")

    # Przykład użycia:
    expected = 0.25773575641192964  # moc wyliczona
    measured = 0.21898980712890626  # moc zmierzona
    upper = 0.01  # 1%
    lower = 0.01  # 1%

    result, msg = check_power_within_limits(expected, measured, upper, lower)
    print(result, msg)

