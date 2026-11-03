#!/usr/bin/env python3
"""
Heru 160T - Modbus TCP Styr- och Avläsningsskript (med Coils för driftlägen)
IP: 192.168.51.202 | Port: 502 | Unit ID: 1
"""

import sys
import argparse
from pymodbus.client import ModbusTcpClient

HERU_IP = "192.168.51.202"
HERU_PORT = 502
UNIT_ID = 1

# Korrekta Modbus Coils (0-baserade adresser för styrsignaler)
COIL_OVERPRESSURE = 1  # 0x00002 i mappen (Övertryck / Eldningsläge)
COIL_BOOST = 2         # 0x00003 i mappen (Forcering)

def connect_client():
    client = ModbusTcpClient(HERU_IP, port=HERU_PORT)
    if not client.connect():
        print(f"❌ Kunde inte ansluta till Heru på {HERU_IP}:{HERU_PORT}")
        sys.exit(1)
    return client

def read_status():
    client = connect_client()
    try:
        print("==================================================")
        print("         HERU 160T - STATUS & TELEMETRI           ")
        print("==================================================")

        # 1. Läs temperaturer (Input Registers 0-3)
        input_res = client.read_input_registers(address=0, count=4, device_id=UNIT_ID)
        if not input_res.isError():
            r = input_res.registers
            parse_temp = lambda v: (v - 65536 if v > 32767 else v) / 10.0
            print("🌡️  TEMPERATURER")
            print(f"  • Utomhusluft:         {parse_temp(r[0]):>6.1f} °C")
            print(f"  • Tilluft:             {parse_temp(r[1]):>6.1f} °C")
            print(f"  • Frånluft (Inne):     {parse_temp(r[2]):>6.1f} °C")
            print(f"  • Avluft:              {parse_temp(r[3]):>6.1f} °C")

        # 2. Läs fläktar (Holding Registers 2 & 3)
        holding_res = client.read_holding_registers(address=0, count=4, device_id=UNIT_ID)
        if not holding_res.isError():
            h = holding_res.registers
            print("\n🌀 FLÄKTAKTIVITET")
            print(f"  • Tilluftsfläkt:        {h[2]:>3} %")
            print(f"  • Frånluftsfläkt:       {h[3]:>3} %")

        # 3. Läs av driftlägen via Coils (0 till 4)
        coils_res = client.read_coils(address=0, count=5, device_id=UNIT_ID)
        if not coils_res.isError():
            c = coils_res.bits
            print("\n⚙️  DRIFTLÄGEN (COILS)")
            print(f"  • Övertryck (Coil 2):   {'PÅ 🔥' if c[1] else 'AV 🛑'}")
            print(f"  • Forcering (Coil 3):   {'PÅ 🚀' if c[2] else 'AV 🛑'}")

    except Exception as e:
        print(f"Fel vid avläsning: {e}")
    finally:
        client.close()
        print("==================================================")

def set_coil(coil_addr, state, mode_name):
    client = connect_client()
    try:
        print(f"Sätter {mode_name} till {'PÅ' if state else 'AV'}...")
        client.write_coil(address=coil_addr, value=state, device_id=UNIT_ID)
        print(f"✅ Kommando skickat för {mode_name}!")
    except Exception as e:
        print(f"Fel vid skrivning av coil: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heru 160T Styrning via Coils")
    parser.add_argument("--boost", choices=["on", "off"], help="Slå på/av Forcering")
    parser.add_argument("--overpressure", choices=["on", "off"], help="Slå på/av Övertryck (Eldningsläge)")

    args = parser.parse_args()

    if args.boost == "on":
        set_coil(COIL_BOOST, True, "Forcering")
    elif args.boost == "off":
        set_coil(COIL_BOOST, False, "Forcering")
    elif args.overpressure == "on":
        set_coil(COIL_OVERPRESSURE, True, "Övertryck")
    elif args.overpressure == "off":
        set_coil(COIL_OVERPRESSURE, False, "Övertryck")
    else:
        read_status()
