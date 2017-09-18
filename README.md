# unlabeledDrumDataset
CW @ GTCMT 2017
Latest update: Sep. 2017


## Introduction 

unlabeledDrumDataset is a collection of unlabeled music for drum transcription task. This repository contains the python implementation of the data collector and .txt files of the youtube links where the audio files can be found online. For related information, please refer to the following publication:

Chih-Wei Wu and Alexander Lerch, Automatic drum transcription using the student-teacher learning paradigm with unlabeled music data, in Proceedings of the International Society of Music Information Retrieval Conference (ISMIR), Suzhou, 2017


## Instruction 

This dataset contains the following folders: {lists, links, src, dataset_for_ismir_2017}.

### links:
This folder includes the list of music video links retrieved from Youtube. Each .txt file includes the links from the specific chart. Each entry follows the format: 

< youtube link > \tab < song index >

### lists: 
This folder includes the list of songs retrieved from the billboard charts. Each .txt file includes the songs from the specific chart. Each entry follows the format: 

< artist name > \tab < song name > \tab < song index >

### src: 
This folder contains the source code for retrieving the list of songs from the billboard chart and the list of video links from youtube. There are three files in this folder: main.py, retrieveFiles.py, retrieveList.py. For the general usage of these files, please refer to main.py. 

### dataset_for_ismir_2017
In our ISMIR2017 paper, only a subset of the links/ lists in the above folders has been used in the experiments. Specifically, four genres, namely R&B/ HipHop, Pop, Rock, and Latin, are selected (each genre contribute 200 songs to this dataset). Each entry follows the format:

< artist name > \tab < song name > \tab < youtube link > \tab < song index >

### Test Environment:
- Mac OSX 10.11.6
- Safari Version 10.0 (11602.1.50.0.10)
- Python 2.7.12

## Dependencies

This repository requires the following python libraries:

- billboard
- editdistance
- bs4
- pafy
- youtube-dl

## Potential Problems

There are some existing issues during the parsing and the downloading processes: 

1. Sometimes, the retrieveList process will break when the number of songs requested by the user cannot be met.
One may decrease the "stepInMonth" argument in the class constructor, however, the general availability of the songs still depends on the archive of Billboard.com.
2. Similarly, the retrieveFiles process might break (possibly due to the occasional bad connections to Youtube). 
To start from where it stops, simply use the input argument startID in the function getYoutubeFiles() to start the download process from any arbitrary point in the list. 

## Contact

Chih-Wei Wu
Georgia Tech Center for Music Technology (GTCMT)
cwu307@gatech.edu

840 McMillan Street
Atlanta, GA, 


