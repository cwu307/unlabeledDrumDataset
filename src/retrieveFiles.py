'''
Retrieve youtube files according to the given list
CW @ GTCMT 2017
'''
import urllib
import urllib2
from bs4 import BeautifulSoup

class YoutubeDownloader:
    mList = []
    mLinks = []

    def __init__(self, inputList):
        self.mList = inputList

    def getYoutubeLinks(self):
        # go through the list and retrieve the top search results
        for chartEntry in self.mList:
            # ==== The source following code: ====
            # http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search
            # Minor modification applied
            searchText = str(chartEntry.title) + str(chartEntry.artist)
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






