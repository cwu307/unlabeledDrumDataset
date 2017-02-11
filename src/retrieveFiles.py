'''
Retrieve youtube files according to the given list
CW @ GTCMT 2017
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import pafy
import os

class YoutubeDownloader:
    mList = []
    mLinks = []

    def __init__(self, chartName, inputListPath):
        inputList = open(inputListPath, 'r')
        self.mChartName = chartName
        for line in inputList.readlines():
            tmp = line.split('    ')
            self.mList.append((tmp[0], tmp[1][0:-1]))

    def getYoutubeLinks(self):
        # go through the list and retrieve the top search results
        for artist, title in self.mList:
            # ==== The source following code: ====
            # http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search
            # Minor modification applied
            searchText = title + ' ' + artist
            query = urllib.quote(searchText)
            url = "https://www.youtube.com/results?search_query=" + query
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            topResults = []
            for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
                youtubeLink = 'https://www.youtube.com' + vid['href']
                topResults.append(youtubeLink)
            # ===============================================
            if len(topResults) >= 1:
                self.mLinks.append(topResults[0])
        return self.mLinks


    def getYoutubeFiles(self, txtFile):
        c = 0
        folderName = self.mChartName
        links = open(txtFile, 'r')
        for url in links.readlines():
            songTitle, artist = self.mList[c]
            #==== get video object
            video = pafy.new(url)
            bestaudio = video.getbestaudio()

            #==== take care of filenames
            tempFilename = 'temp' + '.' + str(bestaudio.extension)
            bestaudio.download(tempFilename)
            folderpath = '../' + folderName
            filename = ''.join(e for e in (songTitle + artist) if e.isalnum())
            outputFilePath = '../' + folderName + '/' + str(filename) + '.mp3'
            if not os.path.isdir(folderpath):
                os.mkdir(folderpath)

            #==== convert temp file into mp3
            command_temp2mp3 = 'ffmpeg -i ' + tempFilename + ' -acodec libmp3lame -ab 128k ' + outputFilePath
            os.system(command_temp2mp3)
            command_cleanup = 'rm ' + tempFilename
            os.system(command_cleanup)
            c += 1

    def writeLinks2txt(self):
        if not os.path.isdir('../links/'):
            os.makedirs(os.path.dirname('../links/'))
        filename = '../links/' + self.mChartName + '_links' + '.txt'
        txtfile = open(filename, 'w')
        for link in self.mLinks:
            txtfile.write((link + '\n'))
        txtfile.close()

    def displayLinks(self):
        for link in self.mLinks:
            print link




