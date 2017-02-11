'''
Main function
This function applies the function in "retrieveList.py" and "retrieveFiles.py"
and generate the unlabeled data for drum transcription experiments
CW @ GTCMT 2017
'''
import retrieveList as rl
import retrieveFiles as rf

#==== Enter valid chart names such as:
# rock-songs; alternative-songs; pop-songs; adult-pop-songs; r-b-hip-hop-songs;
# r-and-b-songs; latin-songs; latin-pop-songs; dance-electronic-songs; dance-club-play-songs
chartName = 'pop-songs'
# Retriever = rl.BillboardRetriever(chartName, '2017-01-24', 1, 2000)
# List = Retriever.getList()
# Retriever.writeList2txt()

#==== Retrieve the youtube links
listpath = '../lists/pop-songs_2017-01-24.txt'
Downloader = rf.YoutubeDownloader(chartName, listpath)
links = Downloader.getYoutubeLinks()

Downloader.displayLinks()
Downloader.writeLinks2txt()
print 'The final length of the youtube links %d' % len(links)

#==== Download the files into the folder named after the Chart
# Downloader.getYoutubeFiles('../links/pop-songs_links.txt')