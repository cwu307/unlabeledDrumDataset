'''
Retrieve selected Billboard list
CW @ GTCMT 2017
'''
import billboard

class BillboardRetriever:
    mMaxSongCount = 0
    mStepInMonth = 0 #
    mList = []
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


        while self.mSongCount < self.mMaxSongCount:
            mm_str = str(mm)
            if len(mm_str) == 1: mm_str = '0' + mm_str

            # retrieve the list using Billboard API
            inputDate = str(yyyy) + '-' + mm_str + '-' + str(dd)
            chart = billboard.ChartData(self.mChartName, inputDate)
            for i in range(0, len(chart)):
                # check for duplications
                if not (str(chart[i].title), str(chart[i].artist)) in self.mList:
                    self.mList.append((str(chart[i].title), str(chart[i].artist)))
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
            if not chart.previousDate:
                break
        return self.mList


    def displayList(self):
        print 'The cumulative list contains %d songs:'%len(self.mList)
        print 'The date of the last chart is %s'%self.mLastDate
        print '================================'
        for title in self.mList:
            print title


    def writeList2txt(self, filename):
        txtfile = open(filename, 'w')
        for title, artist in self.mList:
            txtfile.write((title + '_by_' + artist +'\n'))
        txtfile.close()
