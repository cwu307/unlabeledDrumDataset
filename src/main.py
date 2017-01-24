'''
Main function
This function applies the function in "retrieveList.py" and "retrieveFiles.py"
and generate the unlabeled data for drum transcription experiments
CW @ GTCMT 2017
'''
import retrieveList as rl
import retrieveFiles as rf

# Enter valid chart names such as:
# rock-songs; alternative-songs; pop-songs; adult-pop-songs; r-b-hip-hop-songs;
# r-and-b-songs; latin-songs; latin-pop-songs; dance-electronic-songs; dance-club-play-songs
Retriever = rl.BillboardRetriever('pop-songs', '2017-01-24', 2, 10)
List = Retriever.getList()
Retriever.displayList()


Downloader = rf.YoutubeDownloader(List)
links = Downloader.getYoutubeLinks()

for link in links:
    print link
