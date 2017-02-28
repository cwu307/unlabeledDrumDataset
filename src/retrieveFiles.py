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
            artist = tmp[0]
            title  = tmp[1]
            number = tmp[2][0:-1]
            self.mList.append((artist, title, number))

    def getYoutubeLinks(self):
        # go through the list and retrieve the top search results
        print '==== getting youtube links ===='
        c = 0
        for artist, title, number in self.mList:
            url = self.getUrlWithBestaudio(artist, title)
            self.mLinks.append((url, number))
            c += 1
            print '%d' % c
            print url
        return self.mLinks


    def getYoutubeFiles(self, txtFile, startID):
        folderName = self.mChartName
        links = open(txtFile, 'r')
        print '==== getting youtube files ===='
        #==== if init from the txt file, rebuild the link array
        for line in links.readlines():
            tmp = line.split('    ')
            url = tmp[0]
            number = tmp[1][0:-1]
            self.mLinks.append((url, number))

        #==== go through every link in the list and download
        for c in range(startID - 1, len(self.mLinks)):
            url = self.mLinks[c][0]
            artist, title, number  = self.mList[c]
            #==== get video object
            video = pafy.new(url)
            bestaudio = video.getbestaudio()

            #==== take care of filenames
            tempFilename = 'temp' + '.' + str(bestaudio.extension)
            bestaudio.download(tempFilename)
            folderpath = '../audio/' + folderName
            filename = ''.join(e for e in (title + artist) if e.isalnum())
            outputFilePath = '../audio/' + folderName + '/' + str(number) + '_' + str(filename) + '.mp3'
            if not os.path.isdir(folderpath):
                os.mkdir(folderpath)

            #==== convert temp file into mp3
            command_temp2mp3 = 'ffmpeg -i ' + tempFilename + ' -acodec libmp3lame -ab 128k -ar 44100 ' + outputFilePath
            os.system(command_temp2mp3)
            command_cleanup = 'rm ' + tempFilename
            os.system(command_cleanup)
            c += 1
            print '%d' % c

    def writeLinks2txt(self):
        print '==== writing youtube link txt ===='
        if not os.path.isdir('../links/'):
            os.makedirs(os.path.dirname('../links/'))
        filename = '../links/' + self.mChartName + '_links' + '.txt'
        txtfile = open(filename, 'w')
        for link, number in self.mLinks:
            if 'user' in link:
                txtfile.write(('====' + '    ' + str(number) + '\n'))
            else:
                txtfile.write((link + '    ' + str(number) + '\n'))
        txtfile.close()

    def displayLinks(self):
        for link, number in self.mLinks:
            print number, link


    def getUrlWithBestaudio(self, artist, title):

        #==== strip special chars but keep space
        title = ''.join(e for e in title if (e.isalnum() or e.isspace()))
        artist = ''.join(e for e in artist if (e.isalnum() or e.isspace()))

        # ==== special case: when the artist name is too long, prune it
        tmp = artist.split(' ')
        if len(tmp) >= 6: #heuristic setting, bad style
            artist = tmp[0] + ' ' + tmp[1] + ' ' + tmp[2]
        # ==== 2) setup query text
        searchText = artist + ' ' + title
        query = urllib.quote(searchText)

        # ==== The source following code: ====
        # http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search
        # Minor modification applied
        #==== build query message
        searchUrl = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(searchUrl)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        topResults = []
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            youtubeLink = 'https://www.youtube.com' + vid['href']
            topResults.append(youtubeLink)

        #==== for every link, check if the audio is downloadable
        for link in topResults:
            video = pafy.new(link)
            bestaudio = video.getbestaudio()
            if bestaudio is not None:
                break
        return link


