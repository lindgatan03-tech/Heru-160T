from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient("192.168.51.202", port=502)
c.connect()
r = c.read_input_registers(address=0, count=8, device_id=1)
names = ["ID (ska vara 10)", "Utomhus", "Tilluft", "Frånluft",
         "Avluft", "Vatten", "Värmeväxlare", "Rum"]
if r.isError():
    print(r)
else:
    for i, v in enumerate(r.registers):
        s = v - 65536 if v > 32767 else v
        print(f"adress {i}  {names[i]:<18} rå={v:<6} tolkat={s}")
c.close()
