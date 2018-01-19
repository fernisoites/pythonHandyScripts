# this script aims at working on Mac OS, for other operation system needs to change _FIREFOX_LOC variable
# prerequisite: make sure geckodriver is downloaded and put in same directory
# download url: https://github.com/mozilla/geckodriver/releases

import sys, time, requests
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

_FIREFOX_LOC = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

class Episode:
    def __init__(self, url, stId, parentDir, episodeName):
        self.url = url
        self.stId = stId
        self.directory = os.path.join(parentDir, episodeName)
        self.episodeName = episodeName
        self.fileName = "{}{}.mp4".format(episodeName, stId)
        self.fileFullPath = os.path.join(self.directory, self.fileName)

#download video from url to given filename
#sample url: "http://www.dnvod.tv/Movie/detail.aspx?id=izUp3%2FnFhtY%3D"
#driver is web driver
def downloadFromEpisode(episode, driver = None):
    if not driver: driver = getDriver()
    if not episode or not episode.url:
        print "Error: no url provided!"
        driver.close()
        return
    
    if not os.path.exists(episode.directory):
        os.makedirs(episode.directory)
    
    if os.path.exists(episode.fileFullPath):
        print "File exist, skip downloading"
        driver.close()
        return

    print "Processing url: {}".format(episode.url)
    driver.get(episode.url)

    found = False
    while not found:
        d = driver.page_source.encode('utf-8')

        rgst = d.split('src="')
        for st in rgst:
            for short in st.split('" id'):
                if ".mp4" in short and "sourceIp" in short and "signature" in short:
                    found = True
                    trueUrl = short.replace("&amp;", "&")
                    print "downloading to:\n{}\nfrom:\n{}".format(episode.fileFullPath, trueUrl)
                    r = requests.get(trueUrl, allow_redirects= True)
                    open(episode.fileFullPath, 'wb').write(r.content)

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

def getEpisodeFromHtml(html, parentDir = "", episodeName = ""):
    rg = []

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

    for episodeHtml in target.split("</a>"):
        stId = episodeHtml[-2:]
        if not stId.isdigit(): continue

        stPartialUrl = episodeHtml[episodeHtml.index("Readyplay"):(episodeHtml.index('%3d')+3)]
        stUrl = "http://www.dnvod.tv/Movie/{}".format(stPartialUrl)
        
        episode = Episode(stUrl, stId, parentDir, episodeName)
        rg.append(episode)
    return rg

#get web driver
def getDriver(absdFirefox = _FIREFOX_LOC, ):
    binary = FirefoxBinary(absdFirefox)
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver

def main():
    global _FIREFOX_LOC
    targetDir = ""
    episodeName = ""
    if len(sys.argv) == 1: 
        print "Error: expect url paramter"
        return
    _URL = sys.argv[1]
    if len(sys.argv) > 2:
        episodeName = sys.argv[2]
    if len(sys.argv) > 3:
        targetDir = sys.argv[3]
        
    html = getHtmlFromUrl(_URL)
    rg = getEpisodeFromHtml(html, targetDir, episodeName)
    rg = sorted(rg, key = lambda episode : int(episode.stId))
    for episode in rg:
        downloadFromEpisode(episode)
    
if __name__ == "__main__":
    main()