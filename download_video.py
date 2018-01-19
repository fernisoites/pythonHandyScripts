import sys, time, requests
import os.path
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

_FIREFOX_LOC = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

#download video from url to given filename
#sample url: "http://www.dnvod.tv/Movie/detail.aspx?id=izUp3%2FnFhtY%3D"
#driver is web driver
def downloadFromUrl(url, fileName, driver = None):
    if not driver: driver = getDriver()
    if not url: 
        print "Error: no url provided!"
        return

    print "Processing url: {}".format(url)
    driver.get(url)

    found = False
    while not found:
        d = driver.page_source.encode('utf-8')

        rgst = d.split('src="')
        for st in rgst:
            for short in st.split('" id'):
                if ".mp4" in short and "sourceIp" in short and "signature" in short:
                    found = True
                    trueUrl = short.replace("&amp;", "&")
                    print "downloading from:\n{}".format(trueUrl)
                    r = requests.get(trueUrl, allow_redirects= True)
                    open(fileName, 'wb').write(r.content)

        time.sleep(10)
    
    driver.close()

def getHtmlFromUrl(url, driver = None):
    if not driver: driver = getDriver()
    if not url: 
        print "Error: no url provided!"
        return
    
    driver.get(url)
    d = driver.page_source.encode('utf-8')

    driver.close()
    
    return d

def getUrlMapFromHtml(html, targetDir = ""):
    mp = {}

    #get portion of html containing all Urls and Ids
    target = ""
    for portion in html.split('</select>'):
        if 'ref="Readyplay.aspx?' not in portion: continue
        else:
            target = portion
            break

    #normalize target
    target = target.replace('</div></div></li><li><div class="bfan-n"><div class="bfan-n">', '')
    target = target.replace('</div></div></li><li style="display: none;"><div class="bfan-n"><div class="bfan-n">', '')

    for episode in target.split("</a>"):
        stId = episode[-2:]
        if not stId.isdigit(): continue

        stPartialUrl = episode[episode.index("Readyplay"):(episode.index('%3d')+3)]
        stUrl = "http://www.dnvod.tv/Movie/{}".format(stPartialUrl)
        stFileName = "{}{}.mp4".format(targetDir, stId)
    
        mp[stFileName] = stUrl
    
    return mp

#get web driver
def getDriver(absdFirefox = _FIREFOX_LOC, ):
    binary = FirefoxBinary(absdFirefox)
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver

def main():
    global _FIREFOX_LOC
    targetDir = "/Volumes/USB_Storage/episodes/"
    if len(sys.argv) == 1: 
        print "Error: expect url paramter"
        return
    _URL = sys.argv[1]
    if len(sys.argv) > 2:
        targetDir = os.path.join(targetDir, sys.argv[2], sys.argv[2])

    html = getHtmlFromUrl(_URL)
    mp = getUrlMapFromHtml(html, targetDir)
    for stFileName, stUrl in mp.iteritems():
        downloadFromUrl(stUrl, stFileName)
    
if __name__ == "__main__":
    main()