# Heru 160T - Modbus TCP Control & Telemetry

Python-skript (`heru_control.py`) för avläsning av status samt remote-styrning av Heru 160T ventilationsaggregat via Modbus TCP.

## Enhetskonfiguration

* **IP-adress:** `192.168.51.202`
* **Port:** `502`
* **Unit ID (Modbus Slave ID):** `1`

## Starta i terminalen (Vid ny session eller omstart)

Om du öppnar ett nytt terminalfönster behöver du gå till projektmappen och aktivera den virtuella Python-miljön (`venv`) innan du kör kommandona:

```bash
# 1. Gå till projektmappen
cd ~/heru

# 2. Aktivera virtual environment
source venv/bin/activate
```

*(Du ser att miljön är aktiverad när det står `(venv)` längst till vänster i terminalen).*

---

## Användning & Kommandon

### 1. Statusavläsning

Kör skriptet utan argument för att hämta aktuell status för temperaturer, fläkthastigheter och driftlägen:

```bash
python heru_control.py
```

### 2. Driftlägen (Coils)

#### Forcering (Boost)

* **Slå på forcering:**
  ```bash
  python heru_control.py --boost on
  ```

* **Slå av forcering:**
  ```bash
  python heru_control.py --boost off
  ```

#### Övertryck (Eldningsläge)

* **Slå på övertryck:**
  ```bash
  python heru_control.py --overpressure on
  ```

* **Slå av övertryck:**
  ```bash
  python heru_control.py --overpressure off
  ```

### 3. Fläktstyrning (Normaldrift / Procent)

Fläktarna regleras individuellt i procent (0–100 %) via Holding Registers (EC-fläktstyrenhet).

* **Ställ in normalläge (Balanserat flöde: 53 % Tilluft / 54 % Frånluft):**
  ```bash
  python heru_control.py --supply 53 --exhaust 54
  ```

* **Ställ in valfria hastigheter:**
  ```bash
  python heru_control.py --supply <PROCENT> --exhaust <PROCENT>
  ```
  *(Ersätt `<PROCENT>` med valt värde mellan 0 och 100)*