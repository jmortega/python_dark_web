import requests
import socket
import socks

# Following prints your normal public IP
print(requests.get("http://httpbin.org/ip").text)

socks.set_default_proxy(socks.SOCKS5, "localhost",9050)
socket.socket = socks.socksocket

# All requests will pass through the SOCKS proxy
# Should print an IP different than your public IP
print(requests.get("http://httpbin.org/ip").text)




