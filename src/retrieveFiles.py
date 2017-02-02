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

    def __init__(self, inputList):
        self.mList = inputList

    def getYoutubeLinks(self):
        # go through the list and retrieve the top search results
        for title, artist in self.mList:
            # ==== The source following code: ====
            # http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search
            # Minor modification applied
            searchText = title + artist
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

            self.mLinks.append(topResults[0])
        return self.mLinks


    def getYoutubeFiles(self, links, folderName):

        for url in links:
            #==== get video object
            video = pafy.new(url)
            bestaudio = video.getbestaudio()

            #==== take care of filenames
            tempFilename = 'temp' + '.' + str(bestaudio.extension)
            bestaudio.download(tempFilename)
            folderpath = '../' + folderName
            filename = ''.join(e for e in bestaudio.title if e.isalnum())
            outputFilePath = '../' + folderName + '/' + str(filename) + '.mp3'
            if not os.path.isdir(folderpath):
                os.mkdir(folderpath)

            #==== convert temp file into mp3
            command_temp2mp3 = 'ffmpeg -i ' + tempFilename + ' -acodec libmp3lame -ab 128k ' + outputFilePath
            os.system(command_temp2mp3)
            command_cleanup = 'rm ' + tempFilename
            os.system(command_cleanup)







