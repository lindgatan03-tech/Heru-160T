from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient(
    "192.168.51.202", 
    port=502, 
    source_address=("192.168.51.84", 0), 
    timeout=3
)

print("Försöker ansluta...")
connected = c.connect()
print("Ansluten:", connected)

if connected:
    try:
        # Läs av 10 register med början på adress 0
        r = c.read_holding_registers(address=0, count=10, device_id=1)
        if not r.isError():
            print("Registervärden (0-9):", r.registers)
        else:
            print("Modbus-fel:", r)
    except Exception as e:
        print("Fel vid läsning:", e)
    finally:
        c.close()
else:
    print("Kunde inte ansluta.")

