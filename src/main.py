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
Retriever = rl.BillboardRetriever(chartName, '2017-01-24', 2, 100)
List = Retriever.getList()

#==== Retrieve the youtube links
Downloader = rf.YoutubeDownloader(List)
links = Downloader.getYoutubeLinks()

Retriever.displayList()
for link in links:
    print link

#==== Download the files into the folder named after the Chart
Downloader.getYoutubeFiles(links, chartName)