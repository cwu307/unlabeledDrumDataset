'''
Retrieve selected Billboard list
CW @ GTCMT 2017
'''
import billboard
import editdistance
import os

class BillboardRetriever:
    mMaxSongCount = 0
    mStepInMonth = 0 #
    mList = []
    mListPrint = []
    mSongCount = 0
    mStartDate = '' # format: yyyy-mm-dd
    mLastDate  = ''

    def __init__(self, chartName, startDate, stepInMonth, maxSongCount):
        self.mChartName = chartName
        self.mStepInMonth = stepInMonth
        self.mMaxSongCount = maxSongCount
        self.mStartDate = startDate

    def getList(self):
        yyyy = int(self.mStartDate[0:4])
        mm = int(self.mStartDate[5:7])
        dd = int(self.mStartDate[8:])

        # inputDate = self.mStartDate
        preSongCount = []
        while self.mSongCount < self.mMaxSongCount:
            preSongCount.append(self.mSongCount)
            print self.mSongCount
            mm_str = str(mm)
            if len(mm_str) == 1: mm_str = '0' + mm_str

            # retrieve the list using Billboard API
            inputDate = str(yyyy) + '-' + mm_str + '-' + str(dd)

            chart = billboard.ChartData(self.mChartName, inputDate)
            for i in range(0, len(chart)):
                # check for duplications
                # 1) remove special characters
                title = str(chart[i].title)
                title = ''.join(e for e in title if e.isalnum())
                artist = str(chart[i].artist)
                artist = ''.join(e for e in artist if e.isalnum())

                # 2) all lower cases
                title = title.lower()
                artist = artist.lower()

                # 3) compute edit distance
                all_dist = []
                for e1, e2 in self.mList:
                    d1 = editdistance.eval(artist, e1)
                    d2 = editdistance.eval(title, e2)
                    all_dist.append((d1 + d2))

                # 4) add to the list depending on the editdistance
                if len(all_dist) == 0:
                    self.mList.append((artist, title))
                    self.mListPrint.append((str(chart[i].artist), str(chart[i].title)))
                    self.mSongCount += 1
                    if self.mSongCount >= self.mMaxSongCount:
                        break
                #elif (artist, title) not in self.mList and min(all_dist) >= 16:
                elif len([pair for pair in self.mList if title in pair]) == 0 and min(all_dist) >= 12:
                    # check the name of the title as well
                    self.mList.append((artist, title))
                    self.mListPrint.append((str(chart[i].artist), str(chart[i].title)))
                    self.mSongCount += 1
                    if self.mSongCount >= self.mMaxSongCount:
                        break

            # set a new date
            if mm - self.mStepInMonth <= 0: yyyy -= 1
            if self.mStepInMonth >= mm:
                mm_new = ((mm + 12) - self.mStepInMonth) % 12
            elif self.mStepInMonth < mm:
                mm_new = (mm - self.mStepInMonth) % 12
            if mm_new == 0: mm_new = 12
            mm = mm_new

            self.mLastDate = inputDate
            # if chart.previousDate:
            #     inputDate = chart.previousDate
            # else:
            #     break
            # stop the loop if the number of songs stop changing for 3 iterations
            if float(sum(preSongCount[-3:]))/3.0 == self.mSongCount:
                break

        # sort the list before return
        self.mList.sort()
        self.mListPrint.sort()
        return self.mList


    def displayList(self):
        print 'The cumulative list contains %d songs:'%len(self.mList)
        print 'The date of the last chart is %s'%self.mLastDate
        print '================================'
        for artist, title in self.mListPrint:
            print artist, title


    def writeList2txt(self):
        if not os.path.isdir('../lists/'):
            os.makedirs(os.path.dirname('../lists/'))
        filename = '../lists/' + self.mChartName + '_' + self.mStartDate + '.txt'
        txtfile = open(filename, 'w')
        number = 0
        for artist, title in self.mListPrint:
            number += 1
            txtfile.write((artist + '    ' + title + '    ' + str(number) + '\n'))
        txtfile.close()
