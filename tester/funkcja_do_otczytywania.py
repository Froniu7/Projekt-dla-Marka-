import re

def extract_reactive_value(text: str):
    import re
    """
    Odczytuje wartość pojemności (uF) lub indukcyjności (mH) z podanego stringa.
    Zwraca słownik {'type': 'C', 'value': 15.0, 'unit': 'uF'} lub {'type': 'L', 'value': 407.44, 'unit': 'mH'}
    Jeśli nie znajdzie wartości, zwraca None.
    """

    # Wzorce dla pojemności i indukcyjności
    cap_pattern = re.compile(r"([\d.,]+)\s*\[\s*uF\s*\]", re.IGNORECASE)
    ind_pattern = re.compile(r"([\d.,]+)\s*\[\s*mH\s*\]", re.IGNORECASE)

    # Szukamy pojemności
    cap_match = cap_pattern.search(text)
    if cap_match:
        value = float(cap_match.group(1).replace(",", "."))
        return {"type": "C", "value": value, "unit": "uF"}

    # Szukamy indukcyjności
    ind_match = ind_pattern.search(text)
    if ind_match:
        value = float(ind_match.group(1).replace(",", "."))
        return {"type": "L", "value": value, "unit": "mH"}

    # Jeśli nic nie znaleziono
    return None

wartosc=extract_reactive_value("0.5 [kVAr], 15 [uF] Wima")
print(wartosc)
wartosc=extract_reactive_value("5 [kVAr] 440 V, 4 [kVAr] 400 V, 26.53 [uF] CIRCUTOR CLZ-FPT")
print(wartosc)
wartosc=extract_reactive_value("1.5 [kVAr], 407.44 [mH] ABB")
print(wartosc)

