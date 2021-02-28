import time
import socket
from struct import pack

version = 1

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
}

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = pack('>I', len(string))
	for i in string:
		a = key ^ ord(i)
		key = a
		result += bytes([a])
	return result


def send(ip, port, cmd):
	# Send command and receive reply
	try:
		sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock_tcp.settimeout(10)
		sock_tcp.connect((ip, port))
		sock_tcp.settimeout(None)
		sock_tcp.send(encrypt(cmd))
		data = sock_tcp.recv(2048)
		sock_tcp.close()

	except socket.error:
		quit("Could not connect to host " + ip + ":" + str(port))


# Set target IP, port and command to send
ip = "192.168.2.27"
port = 9999
cmd = commands['off']

print("Turning off Cable Modem")
send(ip, port, cmd)

time.sleep(5)
cmd = commands['on']

print("Turning on Cable Modem")
send(ip, port, cmd)