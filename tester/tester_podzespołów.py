from pymodbus.client.sync import ModbusSerialClient  # <<< zmiana
import struct

# Funkcja pomocnicza do konwersji rejestrów 16-bit -> float32
def regs_to_float(registers):
    if not registers or len(registers) < 2:
        return None
    return struct.unpack('>f', struct.pack('>HH', registers[0], registers[1]))[0]

# Konfiguracja klienta Modbus RTU
client = ModbusSerialClient(
    method="rtu",
    port="COM3",
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity="N",
    timeout=1
)

if not client.connect():
    print("❌ Brak połączenia z urządzeniem!")
    exit(1)

slave_id = 1

volt_regs = {"U1": 4352, "U2": 4354, "U3": 4356}
curr_regs = {"I1": 4608, "I2": 4610, "I3": 4612}
reactive_regs = {"Q1": 4868, "Q2": 4870, "Q3": 4872}

def read_float(address):
    rr = client.read_input_registers(address=address, count=2, unit=slave_id)
    if rr.isError():
        return None
    return regs_to_float(rr.registers)

print("⚡ Odczyt danych z Novar 2700:")

for name, addr in volt_regs.items():
    print(f"{name}: {read_float(addr):.2f} V")

for name, addr in curr_regs.items():
    print(f"{name}: {read_float(addr):.2f} A")

for name, addr in reactive_regs.items():
    print(f"{name}: {read_float(addr):.2f} var")

client.close()
