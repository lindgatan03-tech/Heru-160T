import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)

try:
    print("Försöker ansluta via rå TCP-socket till 192.168.51.202:502...")
    sock.connect(("192.168.51.202", 502))
    print("SUCCÈ: Rå TCP-anslutning lyckades!")
    sock.close()
except Exception as e:
    print("MISSLYCKADES med fel:", e)
