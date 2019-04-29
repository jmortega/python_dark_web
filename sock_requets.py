import requests

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5h://127.0.0.1:9050','https': 'socks5h://127.0.0.1:9050'}
    return session

# Following prints your normal public IP
print(requests.get("http://httpbin.org/ip").text)

# Make a request through the Tor connection
# IP visible through Tor
# Should print an IP different than your public IP
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)

r = session.get('https://www.facebookcorewwwi.onion/')
#get headers dictionary
for key,value in r.headers.items():
    print(key,value)


