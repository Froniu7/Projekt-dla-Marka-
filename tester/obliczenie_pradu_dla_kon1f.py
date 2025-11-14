import math

#obliczenia dla kondensatora 3 fazowego
#**********************************************************************************************************************




def calculate_capacitor_power_delta(C_uF, U, fn):
    """
    Oblicza całkowitą moc kondensatora w połączeniu w trójkąt, przyjmując pojemność w µF.

    Args:
      C_uF (float): Pojemność pojedynczego kondensatora w mikrofaradach (µF).
      U (float): Napięcie międzyfazowe w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Całkowita moc kondensatora w kilovoltamperach reaktywnych (kVar).
    """
    C_F = C_uF * 1e-6
    Qc = 3 * C_F * (U ** 2) * 2 * math.pi * fn
    Qc_kvar = Qc / 1000
    return Qc_kvar


def calculate_line_current(C_uF, U, fn):
    """
    Oblicza prąd liniowy dla banku kondensatorów połączonych w trójkąt.

    Args:
      C_uF (float): Pojemność pojedynczego kondensatora w mikrofaradach (µF).
      U (float): Napięcie międzyfazowe w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Prąd liniowy w amperach (A).
    """
    # Obliczenie całkowitej mocy (w Var)
    Qc_var = calculate_capacitor_power_delta(C_uF, U, fn) * 1000

    # Obliczenie prądu liniowego I_L = Qc / (sqrt(3) * U_L)
    I_L = Qc_var / (math.sqrt(3) * U)

    return I_L


# Przykład użycia z tabeli (wiersz 6, pojemność 3 x 27,4 µF, 400 V, 50 Hz)
C_uF_example = 40.3
U_example = 408
fn_example = 50

line_current = calculate_line_current(C_uF_example, U_example, fn_example)

print(f"Całkowita moc kondensatora: {calculate_capacitor_power_delta(C_uF_example, U_example, fn_example):.2f} kVar")
print(f"Prąd liniowy dla tego kondensatora wynosi: {line_current:.2f} A")

# Sprawdzenie z tabelą
# Tabela dla 400V, pojemność 3x27.4 uF (oznaczenie 5 kVar)
# Prąd podany w tabeli: 5.9 A
# Nasz wynik to ~5.95 A. Mała różnica wynika z zaokrągleń w tabeli.


#obliczenia dla kondensatora 1 fazowego :
import math

# Ponowne użycie funkcji do obliczenia mocy
def calculate_single_phase_power(C_uF, U, fn):
  """
  Oblicza moc kondensatora jednofazowego.
  """
  C_F = C_uF * 1e-6
  Qc = C_F * (U**2) * 2 * math.pi * fn
  Qc_kvar = Qc / 1000
  return Qc_kvar

def calculate_single_phase_current(C_uF, U, fn):
  """
  Oblicza prąd płynący przez kondensator jednofazowy.

  Args:
    C_uF (float): Pojemność kondensatora w mikrofaradach (µF).
    U (float): Napięcie w woltach (V).
    fn (float): Częstotliwość w hercach (Hz).

  Returns:
    float: Prąd w amperach (A).
  """
  # Obliczenie mocy w var (Wartość Q w Var jest używana do obliczenia prądu)
  power_var = calculate_single_phase_power(C_uF, U, fn) * 1000

  # Obliczenie prądu I = Q / U
  current_A = power_var / U

  return current_A

# Przykład użycia
C_example = 120.4
U_example = 230
fn_example = 50

current_A = calculate_single_phase_current(C_example, U_example, fn_example)

print(f"Prąd płynący przez kondensator jednofazowy wynosi: {current_A:.2f} A")

#obliczenie mocy dławika 1 fazowego :

import math


def calculate_single_phase_inductor_power_mH(L_mH, U, fn):
    """
    Oblicza moc bierną dławika jednofazowego, przyjmując indukcyjność w milihenrach (mH).

    Args:
      L_mH (float): Indukcyjność dławika w milihenrach (mH).
      U (float): Napięcie zasilania w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Moc bierna dławika w kilovoltamperach reaktywnych (kVar).
    """
    # Przeliczenie indukcyjności z mH na H
    L_H = L_mH * 1e-3

    # Obliczenie reaktancji indukcyjnej XL
    XL = 2 * math.pi * fn * L_H

    # Obliczenie mocy biernej QL = U^2 / XL
    QL = (U ** 2) / XL

    # Przeliczenie na kVar
    QL_kvar = QL / 1000

    return QL_kvar


def calculate_single_phase_inductor_current_mH(L_mH, U, fn):
    """
    Oblicza prąd płynący przez dławik jednofazowy, przyjmując indukcyjność w milihenrach (mH).

    Args:
      L_mH (float): Indukcyjność dławika w milihenrach (mH).
      U (float): Napięcie zasilania w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Prąd w amperach (A).
    """
    # Obliczenie mocy w var (moc jest potrzebna do obliczenia prądu)
    power_var = calculate_single_phase_inductor_power_mH(L_mH, U, fn) * 1000

    # Obliczenie prądu I = QL / U
    current_A = power_var / U

    return current_A


# Przykład użycia:
# Dane:
L_example_mH = 67.5  # Indukcyjność w mH
U_example_V = 230  # Napięcie w V
fn_example_Hz = 50  # Częstotliwość w Hz

power_kvar = calculate_single_phase_inductor_power_mH(L_mH=L_example_mH, U=U_example_V, fn=fn_example_Hz)
current_A = calculate_single_phase_inductor_current_mH(L_mH=L_example_mH, U=U_example_V, fn=fn_example_Hz)

print(f"Moc bierna dławika: {power_kvar:.2f} kVar")
print(f"Prąd płynący przez dławik: {current_A:.2f} A")


#obliczenia dla dławika 3 fazowego

import math


def calculate_three_phase_inductor_power(L_mH, U, fn):
    """
    Oblicza całkowitą moc bierną dławika trójfazowego,
    zakładając połączenie w gwiazdę.

    Args:
      L_mH (float): Indukcyjność dławika w milihenrach (mH) - wartość na fazę.
      U (float): Napięcie międzyfazowe w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Całkowita moc bierna dławika w kilovoltamperach reaktywnych (kVar).
    """
    # Przeliczenie indukcyjności z mH na H
    L_H = L_mH * 1e-3

    # Obliczenie reaktancji na fazę
    XL = 2 * math.pi * fn * L_H

    # Obliczenie napięcia fazowego (dla połączenia w gwiazdę)
    U_phase = U / math.sqrt(3)

    # Obliczenie mocy na fazę
    Q_phase = (U_phase ** 2) / XL

    # Obliczenie całkowitej mocy (razy 3 fazy)
    Q_total = 3 * Q_phase

    # Przeliczenie na kVar
    Q_total_kvar = Q_total / 1000

    return Q_total_kvar


def calculate_three_phase_inductor_current(L_mH, U, fn):
    """
    Oblicza prąd liniowy dławika trójfazowego,
    zakładając połączenie w gwiazdę.

    Args:
      L_mH (float): Indukcyjność dławika w milihenrach (mH) - wartość na fazę.
      U (float): Napięcie międzyfazowe w woltach (V).
      fn (float): Częstotliwość w hercach (Hz).

    Returns:
      float: Prąd liniowy w amperach (A).
    """
    # Obliczenie całkowitej mocy w var
    power_var = calculate_three_phase_inductor_power(L_mH, U, fn) * 1000

    # Obliczenie prądu liniowego IL = Q_total / (sqrt(3) * U_L)
    current_A = power_var / (math.sqrt(3) * U)

    return current_A


# Przykład użycia:
# Załóżmy dławik 3-fazowy o indukcyjności 10 mH na fazę
# Napięcie międzyfazowe: 400 V
# Częstotliwość: 50 Hz

L_example_mH = 102
U_example_V = 400
fn_example_Hz = 50

power_kvar = calculate_three_phase_inductor_power(L_mH=L_example_mH, U=U_example_V, fn=fn_example_Hz)
current_A = calculate_three_phase_inductor_current(L_mH=L_example_mH, U=U_example_V, fn=fn_example_Hz)

print(f"Całkowita moc bierna dławika 3-fazowego (gwiazda) wynosi: {power_kvar:.2f} kVar")
print(f"Prąd liniowy dla tego dławika wynosi: {current_A:.2f} A")

