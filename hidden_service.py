import requests

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5h://127.0.0.1:9050','https': 'socks5h://127.0.0.1:9050'}
    return session

def searchUnderDir(address,session):
    for page in range(1,5):
        for searchItem in ['bitcoin']:
            addressWithCriteria = address.replace("CRITERIA_WILDCARD",searchItem)
            #http://underdj5ziov3ic7.onion/search/bitcoin/pg/1
            addressToSearch = addressWithCriteria + "/"+ str(page)
            print(addressToSearch)
            response = session.get(address)
            print(response)
            print(response.text)
            
# Following prints your normal public IP
print(requests.get("http://httpbin.org/ip").text)

# Make a request through the Tor connection
# IP visible through Tor
# Should print an IP different than your public IP
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)

searchUnderDir('http://underdj5ziov3ic7.onion/search/CRITERIA_WILDCARD/pg',session)

#http://underdj5ziov3ic7.onion/category/HACKING

