
from time import sleep
from interruptingcow import timeout
import sys
from bs4 import BeautifulSoup
import requests
import os
    
# -------------------- REQUEST SESSION PROXIES --------------------

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5h://127.0.0.1:9050','https': 'socks5h://127.0.0.1:9050'}
    return session


def crawl(option, deeplinks, link, intexts, session):
    error=0
    if option is "default":
        length_of_web_links_to_crawl = len(deeplinks)
        iterations = 0
        
        while len(deeplinks) <= number_results or length_of_web_links_to_crawl <= iterations:
            try:
                with timeout(10):
                    crawl = session.get(deeplinks[iterations])
            except:
                error=1
            if not error:
                crawl = crawl.text
                try:
                    soup = BeautifulSoup(crawl, "lxml")
                except:
                    print("Error creating 'soup' object")
                    os.system("sudo service tor stop")
                    exit()
                
                for a in soup.find_all('a', href=True):
                    if len(deeplinks) >= number_results:
                        print(" \033[0;32m LINKS COLLECTED!\033[0m")
                        os.system("sudo service tor stop")
                        exit()
                    darklink = isValidOnionAdress(deeplinks[iterations],session)    
                    if darklink:
                        if not darklink in deeplinks:
                            if intexts in crawl or intexts == "":        
                                print(darklink)
                            else:
                                print("valid link, but have not '" + intexts + "' inside: \033[0;31m" + darklink + "\033[0m")   
                iterations+=1      
    if option is "all":
        try:
            with timeout(10):
                crawl = session.get(link)
        except:
            error = 1
        if not error:
            crawl = crawl.text
            try:
                soup = BeautifulSoup(crawl, "lxml")
            except:
                print("Error creating 'soup' object")
                os.system("sudo service tor stop")
                exit()
            print("Crawling from : " + "[\033[0;31m" + link + "\033[0m]")
            for a in soup.find_all('a', href=True):
                if len(deeplinks) >= number_results:     
                    print(" \033[0;32m LINKS COLLECTED!\033[0m")
                    os.system("sudo service tor stop")
                    exit()
                    
                darklink = isValidOnionAdress(a['href'],session)   
                if darklink:
                    if not darklink in deeplinks:
                        if intexts in crawl or intexts == "":
                            deeplinks.append(darklink)
                            print(darklink)
                        else: 
                            print("valid link, but have not '" + intexts + "' inside: \033[0;31m" + darklink + "\033[0m")   
        else:
            print("Skipping, takes to long")

def isValidOnionAdress(darklink,session):
    if not ".onion" in darklink: # if there's not ".onion" in href
        return False
        
    if "http://" in darklink: # if we are here, the link contains a .onion so, lets 'clean' it
        isvalid = darklink.split("http://")[1].split(".onion")[0]
        isvalid = "http://" + isvalid + ".onion"
        print(isvalid)
        try:
            with timeout(10):
                maybevalid = session.get(isvalid) # can we connect to it?
        except:
            return False
        if maybevalid.status_code is not 200:
            return False
        else:
            return isvalid
                
def search(crawling, intexts, session):
    darklinks = []
    
    print("Searching. . . ")

    #process first 5 pages
    for page in range(1,5):
        #http://underdj5ziov3ic7.onion/search/bitcoin/pg
        #http://www.xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi?s=DRP&q=bitcoin
        search_query = "http://underdj5ziov3ic7.onion/search/"+search_string+"/pg/"+str(page)
        #search_query = "http://www.xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi?s=DRP&q="+search_string+"&np="+str(page)

        print("Search query",search_query)
        try:
            content = session.get(search_query)
            content = content.text
        except:
            print("\nError connecting to server")  
            exit()
        try:
            soup = BeautifulSoup(content, "lxml")
        except:
            print("\nError creating 'soup' object")
            os.system("sudo service tor stop")
            exit()
        print(" \033[0;32m [OK]\033[0m")
        print("Checking links ")
        print(soup)
        for a in soup.find_all('a', href=True): # for each href in browser response
            if len(darklinks) >= number_results: # if reached number of links
                print(len(darklinks))
                print("SEARCH COMPLETE" +  "\033[0;32m [OK]\033[0m")
                os.system("sudo service tor stop")
                exit()
            
            darklink = isValidOnionAdress(a['href'],session)
            darklinkd = True
            try:
                contain = session.get(darklink)
                contain = contain.text
            except:
                darklinkd = False
            if darklink and darklinkd: # if valid  
          
                if not darklink in darklinks: # if not present in list
                    if intexts in contain:
                        print(darklink)   
                        darklinks.append(darklink) # add it
                        if "all" in crawling:
                            crawl("all", darklinks, darklink, intexts,session)
                    else:
                        print("valid link, but have not '" + intexts + "' inside: \033[0;31m" + darklink + "\033[0m")   
        if "none" in crawling:
            print("Search completed.")
            exit()
        print("Not enought links in browser, crawling...")
        if darklinks:
            if "default" in crawling:
                crawl("default", darklinks, darklink, intexts,session)
            else:
                print("Not enought links in browser, but crawl disabled")
                os.system("sudo service tor stop")
                exit()
        else:
            print("0 links!, cant crawl...")
            os.system("sudo service tor stop")
            exit()    

def torproxy(session):
    print("Checking Tor instance")
    try:
        print(session.get("http://httpbin.org/ip").text)
    except Exception as exception:
        print(" [\033[0;31mNot connected\033[0m]",exception)
        print("Starting Tor instance ")
        os.system("service tor start")
        sleep(8)
    print(" \033[0;32m [OK]\033[0m")
    print("Checking Tor proxy ")
    try:
        print(session.get("http://httpbin.org/ip").text)
    except Exception as exception:
        print(" => [\033[0;31mERROR\033[0m] proxy is refusing connections",exception)
        os.system("sudo service tor stop")
        exit()
    print(" \033[0;32m [OK]\033[0m")

# -------------------- MAIN PROGRAM --------------------    
if len(sys.argv) not in [4,5] or sys.argv[3] not in ["all", "none", "default"]:
    print("search_dark_web.py SEARCH NUMBER_OF_RESULTS crawl_options intext")
    print("Crawl Options:")
    print("             all) crawl each link")
    print("             none) dont crawl")
    print("             default) crawl if not enough links")

    exit()

    
if __name__ == "__main__":
    try:
        session = get_tor_session()    
        torproxy(session) # set up tor proxy
        search_string = sys.argv[1]
        number_results = int(sys.argv[2])
        crawld = sys.argv[3]
        if len(sys.argv) is 5:
            intext = sys.argv[4]
        else:
            intext = ""
        search(crawld, intext,session)
    except KeyboardInterrupt:
        print("\nExiting. . .")
        os.system("sudo service tor stop")
        exit()
