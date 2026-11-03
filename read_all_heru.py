#!/usr/bin/env python3
"""
Heru 160T - Komplett Modbus TCP Styr- och Avläsningsskript
IP: 192.168.51.202 | Port: 502 | Unit ID: 1
"""

import sys
import argparse
from pymodbus.client import ModbusTcpClient

HERU_IP = "192.168.51.202"
HERU_PORT = 502
UNIT_ID = 1

# Kända registeradresser baserat på verifiering
REG_BOOST = 22        # Forcering (1=PÅ, 0=AV)
REG_OVERPRESSURE = 23 # Plats för övertryck (justeras vid behov)

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
            print(f"  • Utomhusluft (Givare): {r[0]} -> {parse_temp(r[0]):>5.1f} °C")
            print(f"  • Tilluft:             {parse_temp(r[1]):>6.1f} °C")
            print(f"  • Frånluft (Inne):     {parse_temp(r[2]):>6.1f} °C")
            print(f"  • Avluft:              {parse_temp(r[3]):>6.1f} °C")

        # 2. Läs fläktar och kontrollregister (Holding Registers 0-30)
        holding_res = client.read_holding_registers(address=0, count=30, device_id=UNIT_ID)
        if not holding_res.isError():
            h = holding_res.registers
            print("\n🌀 FLÄKTAKTIVITET")
            print(f"  • Tilluftsfläkt:        {h[2]:>5} %")
            print(f"  • Frånluftsfläkt:       {h[3]:>5} %")

            print("\n⚙️  DRIFTLÄGEN")
            boost_status = "PÅ 🚀" if h[REG_BOOST] == 1 else "AV 🛑"
            print(f"  • Forcering (Reg {REG_BOOST}):     {boost_status}")
            print(f"  • Övertryck (Reg {REG_OVERPRESSURE}):    Värde: {h[REG_OVERPRESSURE]}")
            
            print("\n📊 GRUNDINSTÄLLNINGAR (Reg 20-28)")
            print(f"  • Reg 20 (Tilluft forcering?): {h[20]} %")
            print(f"  • Reg 21 (Frånluft forcering?): {h[21]} %")
            print(f"  • Reg 23-28 (Timers/Param):    {h[23:29]}")

    except Exception as e:
        print(f"Fel vid avläsning: {e}")
    finally:
    client.close()
    print("==================================================")

def set_register(reg, value, mode_name):
    client = connect_client()
    try:
        print(f"Sätter {mode_name} (Register {reg}) till {value}...")
        client.write_register(address=reg, value=value, device_id=UNIT_ID)
        
        # Verifiera skrivningen
        res = client.read_holding_registers(address=reg, count=1, device_id=UNIT_ID)
        if not res.isError() and res.registers[0] == value:
            print(f"✅ Verifiering OK: {mode_name} har värdet {value}")
        else:
            actual = res.registers[0] if not res.isError() else "Fel vid läsning"
            print(f"⚠️  Varning: Skrivning utförd, men verifiering visar värde: {actual}")
    except Exception as e:
        print(f"Fel vid skrivning: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heru 160T Styrning")
    parser.add_argument("--boost", choices=["on", "off"], help="Slå på/av Forcering")
    parser.add_argument("--reg", type=int, help="Skriv till ett specifikt register")
    parser.add_argument("--val", type=int, default=1, help="Värde att skriva (standard 1)")

    args = parser.parse_args()

    if args.boost == "on":
        set_register(REG_BOOST, 1, "Forcering")
    elif args.boost == "off":
        set_register(REG_BOOST, 0, "Forcering")
    elif args.reg is not None:
        set_register(args.reg, args.val, f"Register {args.reg}")
    else:
        read_status()
