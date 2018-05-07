# this script aims at working on Mac OS, for other operation system needs to change _FIREFOX_LOC variable
# prerequisite: make sure geckodriver is downloaded and put in same directory
# download url: https://github.com/mozilla/geckodriver/releases

import sys, time, requests
import os, re
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

_FIREFOX_LOC = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"
_REGEX_EIPSODE = r'<a href="(Readyplay.aspx\?id=[0-9a-zA-Z\%]+%3d)" target="_blank" data-id="[0-9]+">([0-9][0-9])</a>'

def _getWebDriver(absdFirefox = _FIREFOX_LOC):
    """get web driver"""
    binary = FirefoxBinary(absdFirefox)
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver

def _getSourceWithWebDriver(url, driver = None):
    if not driver: driver = _getWebDriver()
    if not url: 
        print "Error: no url provided!"
        return
    
    driver.get(url)
    d = driver.page_source.encode('utf-8')
    driver.close()
    
    return d

def _discoverEpisodeFromHtml(html, parentDir = "", episodeName = ""):
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

def _getDownloadUrl(url, driver = None, maxAttempts = 100):
    """
    get download link from url
    sample url: "http://www.dnvod.tv/Movie/detail.aspx?id=izUp3%2FnFhtY%3D"
    """
    if not driver: driver = _getWebDriver()
    driver.get(url)

    downloadUrl, attempts = None, 0
    while downloadUrl == None and attempts < maxAttempts:
        d = driver.page_source.encode('utf-8')
        rgst = d.split('src="')
        for st in rgst:
            for short in st.split('" id'):
                if ".mp4" in short and "sourceIp" in short and "signature" in short:
                    downloadUrl = short.replace("&amp;", "&")
                    
        attempts += 1
        time.sleep(10)
    driver.close()

    return downloadUrl

def _downloadVideo(downloadUrl, destination):
    """
    download video from url to given filename
    sample url: "http://www.dnvod.tv/Movie/detail.aspx?id=izUp3%2FnFhtY%3D"
    """
    dirPath = os.path.dirname(destination)
    if not os.path.exists(dirPath):
        print "Creating directory {}".format(dirPath)
        os.path.mkdirs(dirPath)

    r = requests.get(downloadUrl, allow_redirects= True)
    open(destination, 'wb').write(r.content)

def _getEpisodesUrlFromHtml(html):
    rg = []

    #get portion of html containing all Urls and Ids
    target = ""
    for portion in html.split('</select>'):
        if 'ref="Readyplay.aspx?' not in portion: continue
        
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
        rg.append(stUrl)

    return rg

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
        
    phantomDrive = webdriver.PhantomJS() # this is needed for expanding JS
    html = _getSourceWithWebDriver(_URL, phantomDrive)
    rgUrl = re.findall(_REGEX_EIPSODE, html)
    rgUrlSorted = sorted(rgUrl, key = lambda x : x[1])
    for url, stId in rgUrlSorted:
        url = "http://www.dnvod.tv/Movie/" + url
        destination = os.path.join(targetDir, episodeName, stId + ".mp4")
        if os.path.exists(destination):
            print "Skip downloading {} as it's already been downloaded {}".format(stId, destination)
            continue

        print "Downloading {} from url: {}".format(stId, url)
        downloadUrl = _getDownloadUrl(url)
        print downloadUrl
        _downloadVideo(downloadUrl, destination)
    
if __name__ == "__main__":
    main()
