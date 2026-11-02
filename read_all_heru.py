from pymodbus.client import ModbusTcpClient

IP = "192.168.51.202"
PORT = 502
SOURCE_IP = "192.168.51.84"
DEVICE_ID = 1

client = ModbusTcpClient(IP, port=PORT, source_address=(SOURCE_IP, 0), timeout=3)

print("Försöker ansluta till Heru-aggregatet...")
if client.connect():
    print("Ansluten!\n")

    # 1. Läs temperaturer (Input Registers 0-9)
    in_regs = client.read_input_registers(address=0, count=10, device_id=DEVICE_ID)
    if not in_regs.isError():
        r = in_regs.registers
        print("=== MÄTVÄRDEN - TEMPERATURER ===")
        print(f"Component ID [3x00001]: {r[0]}")
        print(f"Utetemperatur [3x00002]: {r[1] / 10.0} °C")
        print(f"Tilluftstemperatur [3x00003]: {r[2] / 10.0} °C")
        print(f"Frånluftstemperatur [3x00004]: {r[3] / 10.0} °C")
        print(f"Avluftstemperatur [3x00005]: {r[4] / 10.0} °C")
    else:
        print("Kunde inte läsa temperaturer.")

    # 2. Läs fläktdata (Input Registers 20-29)
    fan_regs = client.read_input_registers(address=20, count=10, device_id=DEVICE_ID)
    if not fan_regs.isError():
        fr = fan_regs.registers
        print("\n=== MÄTVÄRDEN - FLÄKTAR ===")
        print(f"Tilluftsfläkt steg [3x00023]: {fr[2]}")
        print(f"Frånluftsfläkt steg [3x00024]: {fr[3]}")
        print(f"Tilluftsfläkt effekt [3x00025]: {fr[4]} %")
        print(f"Frånluftsfläkt effekt [3x00026]: {fr[5]} %")
        print(f"Tilluftsfläkt hastighet [3x00027]: {fr[6]} RPM")
        print(f"Frånluftsfläkt hastighet [3x00028]: {fr[7]} RPM")
    else:
        print("Kunde inte läsa fläktdata.")

    # 3. Läs Holding Registers (börvärden 0-9)
    hold_regs = client.read_holding_registers(address=0, count=10, device_id=DEVICE_ID)
    if not hold_regs.isError():
        hr = hold_regs.registers
        print("\n=== BÖRVÄRDEN (Holding Registers) ===")
        print(f"Temperatursetpunkt (Economy) [4x00001]: {hr[0]} °C")
        print(f"Temperatursetpunkt (Comfort) [4x00002]: {hr[1]} °C")
        print(f"Tilluftsfläkt hastighet EC [4x00003]: {hr[2]} %")
        print(f"Frånluftsfläkt hastighet EC [4x00004]: {hr[3]} %")
    else:
        print("Kunde inte läsa Holding Registers.")

    # 4. Läs Coil Status (Driftlägen: Enhet på, Övertryck, Forcering, Borta)
    coils = client.read_coils(address=0, count=5, device_id=DEVICE_ID)
    if not coils.isError():
        cr = coils.bits
        print("\n=== DRIFTLÄGEN & FUNKTIONER (Coils) ===")
        print(f"Unit on [0x00001]: {cr[0]}")
        print(f"Overpressure mode / Eldning [0x00002]: {cr[1]}")
        print(f"Boost mode / Forcering [0x00003]: {cr[2]}")
        print(f"Away mode / Borta [0x00004]: {cr[3]}")
    else:
        print("Kunde inte läsa Coils.")

    client.close()
else:
    print("Kunde inte ansluta till aggregatet.")
