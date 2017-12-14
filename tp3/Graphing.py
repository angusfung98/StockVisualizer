from tkinter import *
from pandas import *
from copy import *
from decimal import *
import re
import sys
import time
import datetime
import requests


#As we discussed in our meeting, I think you made very little progress between TP1 and TP2.
# With your modified idea, I think you should really focus on working on developing good visualization tools
# for stocks that help the users make decisions on which stocks to buy.
# You should focus mainly on using Tkinter to build such interactive graphs,
# and get your data from CSV files of stock data which you can get easily from Yahoo Finance.
#  You could also use sklearn to do some regressions to learn which stocks might be best to buy and
# visualize the results of this regression using Tkinter as well. I look forward to seeing your progress!

#Algorithimic Plan
#Convert date to a number (number by ordering?)
#put in a 2d list, where each list is a coordinate !
    #maybe a dataframe?
    #n lists, with 2 elements, where n is the number of points
        #element 0 == x (time), element 1 == (price)
#linear mapping to a standard cartesian plane
    #what would be the origin of the system
    #scaling? --> might be adjustable based on multiple of weights
    #linear mapping means a matrix multiplication!
        #check if possible(dimensions work out)
            #can guaranntee by making second matrix 2 by 2
        #each element in resultant matrix is the dot product of corresponding row in first and col in second
            #create dot product helper function that takes matrix A, row, matrix B, col and returns a number
        #dimensions of matrix should be same as original
            #create a resultant matrix with len(matrix A) rows and
#second linear mapping to tkinter coordinate system
    #essentially flipping y so that higher prices have a lower tkinter coordinate value and vice versa
#convert lists into tuples to pass to tkinter
#tkinter points
    #draw lines between points
    #draw axes with scaling
        #find ceiling of highest y, and divide y axis by scaling factor to get necessary number of ticks
        #
#Choose different CSV
#Change date range
#hover to csee info
####Matrix Multiplication ####
class Graph(object):
    def __init__(self, index):
        self.csv = None
        self.index = index
        #linear mapping
        self.xScaling = None
        self.yScaling = None
        self.xOriginal = None
        self.yOriginal = None
        self.xStretch = None
        self.yStretch = None
        self.stretch = None
        self.xOrigin = None
        self.yOrigin = None
        self.priceOrigin = None
        self.url =None
        #Matrices
        self.max = [] #set of all prices
        self.original = [] #original set of prices with their orderings
        self.matrixGraph = [] #list of lists containing coordinates that can be easily manipulated
        self.graph = [] #list of tuples to graph
        #Vectors of x,y of matrices
        self.maxPrice = []
        self.prices = []
        self.maxDate = []
        self.date = []
        self.xMaxOriginalVector = []
        self.yMaxOriginalVector = []
        self.xOriginalVector = []
        self.yOriginalVector = []
        self.xVector = []
        self.yVector = []
        #initializing the values
        self.initialized = False
        self.level = 0
        # printMatrix(A)

    def dotProduct(self, A,row,B,col):
        total = 0
        for i in range(len(A[row])):
            total  += A[row][i] * B[col][i]
        return total

    def matrixMultiply(self, A,B):
        if(len(A[0]) != len(B)): #if cols of A do not equal rows of B, cannot do matrix multiplication
            return None
        else:
            C = [[0,0] for i in range(0,len(A))] #create resultant matrix with 0 entries
            for coordinate in range(0,len(C)):
                for entry in range(0,len(C[0])):
                    C[coordinate][entry] = self.dotProduct(A,coordinate,B,entry) #i,jth entry in C is dot product of
            return C                                                        #ith row in A and jth col in B



    def split_crumb_store(self,v):
        return v.split(':')[2].strip('"')

    def find_crumb_store(self,lines):
        # Looking for
        # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
        for l in lines:
            if re.findall(r'CrumbStore', l):
                return l
        print("Did not find CrumbStore")

    def get_cookie_value(self,r):
        try:
            return {'B': r.cookies['B']}
        except:
            return None
    def get_page_data(self,symbol):
        url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
        r = requests.get(url)
        cookie = self.get_cookie_value(r)

        # Code to replace possible \u002F value
        # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
        # FWP\u002F5EFll3U
        lines = r.content.decode('unicode-escape').strip().replace('}', '\n')
        return cookie, lines.split('\n')

    def get_cookie_crumb(self,symbol):
        cookie, lines = self.get_page_data(symbol)
        crumb = self.split_crumb_store(self.find_crumb_store(lines))
        return cookie, crumb

    def get_data(self,symbol , enddate,cookie, crumb):
        filename = '%s.csv' % (symbol)
        url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=0&period2=%s&interval=1d&events=history&crumb=%s" \
              % (symbol,enddate, crumb)
        response = requests.get(url, cookies=cookie)
        with open(filename, 'wb') as handle:
            for block in response.iter_content(1024):
                handle.write(block)

    def get_now_epoch(self):
        # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
        return int(time.time())
    def download_quotes(self):
        enddate = self.get_now_epoch()
        cookie, crumb = self.get_cookie_crumb(self.index)
        self.get_data(self.index,enddate, cookie, crumb)
    # Above code from https://github.com/bradlucas/get-yahoo-quotes-python/blob/master/get-yahoo-quotes.py

    def csvToMatrix(self):#turn a csv into a matrix of coordinates

        series = Series.from_csv("%s.csv" % (self.index), header=0)
        df = series.to_frame()


        df['Date'] = df.index
        self.prices = series.values.tolist()
        self.date = df.Date.tolist()

        for i in range(len(self.prices)):
            if self.prices[i] == 'null':
                 self.date.pop(i)
        self.prices = [price for price in self.prices if price != 'null'] #https://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating
        self.prices = [float(i) for i in self.prices] #if prices are strings, then set as decimal
        if len(self.maxDate)==0:
            self.maxDate = deepcopy(self.date)
            self.maxPrice = deepcopy(self.prices)
        for i in range(0,len(self.prices)):
            coordinate = [i , self.prices[i]  ]
            self.original.append(coordinate)
        if len(self.max) == 0:
            self.max = deepcopy(self.original) #only do this on first run


    def linearMapping(self,data ): #map A such that it can be displayed on a graph
        height = 2*data.height/3
        width = data.width/2
        #Clear any data from previous graph
        del self.xOriginalVector[:]
        del self.yOriginalVector[:]
        del self.xVector[:]
        del self.yVector[:]
        for i in range(len(self.original)):
             self.xOriginalVector.append(self.original[i][0])
             self.yOriginalVector.append(self.original[i][1])

        self.xOriginal = (max(self.xOriginalVector) - min(self.xOriginalVector)) / 10
        self.yOriginal = (max(self.yOriginalVector) - min(self.yOriginalVector)) / 10
        self.yStretch = height / self.yOriginal
        self.yStretch /= 10 #number of ticks matters
        self.xStretch = width / self.xOriginal
        self.xStretch/=6
        self.stretch = [[self.xStretch,0],[0,self.yStretch]] #stretch factor, how to algorithimically find

        reflect = [[1,0],[0,-1]] #reflection factor so that graph appears correctly
        self.matrixGraph =deepcopy(self.original)
        self.matrixGraph = self.matrixMultiply(self.matrixGraph,self.stretch)
        self.matrixGraph = self.matrixMultiply(self.matrixGraph,reflect)
        for i in range(len(self.matrixGraph)):
            self.xVector.append(self.matrixGraph[i][0])
            self.yVector.append(self.matrixGraph[i][1])
        yShift = - (min(self.yVector) - 25)
        xShift = 100 - min(self.xVector)
        for coordinate in range(len(self.matrixGraph)):#translating the graph
            self.matrixGraph[coordinate][0] += xShift #translate x
            self.matrixGraph[coordinate][1] += yShift  #translate y, algorithmically find
        for i in range(len(self.matrixGraph)):
            self.xVector[i]= self.matrixGraph[i][0]
            self.yVector[i] = self.matrixGraph[i][1]
    def matrixToCoordinates(self): #convert list of lists into list of tuples
        del self.graph[:]
        for coordinate in self.matrixGraph:
            coordinatePair = tuple(coordinate)
            self.graph.append(coordinatePair)


    def drawAxes(self,canvas):

        #Scaling
        self.yScaling = (max(self.yVector) - min(self.yVector)) / 10  # default scaling is one tenth of range of y
        self.xScaling = (max(self.xVector) - min(self.xVector)) / 10  # default scaling is one tenth of range of x
        xOriginal = (max(self.xOriginalVector) - min(self.xOriginalVector)) / 10
        yOriginal = (max(self.yOriginalVector) - min(self.yOriginalVector)) / 10
        #Reference points for drawing


        originX = min(self.xVector)
        originY = max(self.yVector) + self.yScaling
        origin = (originX, originY)  # the origin of our graph is not zero zero in tkinter coordinates

        yAxisPoint = (originX, originY - 11 * self.yScaling)
        xAxisPoint = (originX + 10 * self.xScaling, originY)
        self.xOrigin = originX
        self.yOrigin = originY
        #Drawing the Axis
        canvas.create_line(origin, yAxisPoint)
        canvas.create_line(origin, xAxisPoint)
        #Drawing tick marks
        xTicks = []
        yTicks = []
        for i in range(11):
            xTick = (originX + i * self.xScaling, originY)
            xTicks.append(xTick)
        for i in range(12):
            yTick = (originX, originY - i * self.yScaling)
            yTicks.append(yTick)

        for i in range(11):
            topPoint = (xTicks[i][0] , xTicks[i][1]- 5)
            bottomPoint = (xTicks[i][0] , xTicks[i][1]+ 5)
            canvas.create_line(topPoint, bottomPoint)
            current = round((xTicks[i][0] - self.xOrigin )/self.xStretch)
            dateLabel = "%d-%d-%d" % (self.date[current].month, self.date[current].day,self.date[current].year )
            canvas.create_text(bottomPoint,text = dateLabel, anchor = "n" )
        self.priceOrigin = min(self.yOriginalVector) + -1*self.yOriginal
        for i in range(12):
            leftPoint = (yTicks[i][0]- 5, yTicks[i][1] )
            rightPoint  = (yTicks[i][0]+ 5, yTicks[i][1] )
            canvas.create_line(leftPoint, rightPoint)
            canvas.create_text(leftPoint,text = str("%.2f" %(min(self.yOriginalVector) + (i-1)*self.yOriginal) ), anchor = "e" )

    def lineGrapher(self,canvas ):
        # draw the graph
        for coordinate in range(0,len(self.graph) -1):
            canvas.create_line(self.graph[coordinate],self.graph[coordinate +1])
        #draw the axes
        self.drawAxes(canvas)

    def printMatrix(self,A): #https://stackoverflow.com/questions/39173358/how-to-print-a-matrix-using-python
        for row in A:
            print (' '.join(map(str, row)))

    def draw(self,canvas,data):
       canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='AntiqueWhite1', width=0)
       if( not self.initialized):
            self.initialized = True
            self.download_quotes()
            self.csvToMatrix()
            self.linearMapping( data)
            self.matrixToCoordinates()
       else:
           self.linearMapping(data)
           self.matrixToCoordinates()
       self.lineGrapher(canvas)

    def scaling(self, data, counter):
        self.level += counter
        #rerun the function with the range changed up to the draw method
        print(self.level)
        if(self.level == 0): #0th level is maximum
            #reset date range
            self.original = deepcopy(self.max)
            self.date = deepcopy(self.maxDate)
            self.prices = deepcopy(self.maxPrice)
            print(self.date)

        if(self.level == 1): #1st level is 5 years ago
            self.original = deepcopy(self.max[-5*251:])
            self.date = deepcopy(self.maxDate[-5*251:])
            self.prices = deepcopy(self.maxPrice[-5 * 251:])
            for i in range(len(self.original)):
                self.original[i][0] = i + 1



        if(self.level == 2): #2nd level is 2 years ago
            self.original = deepcopy(self.max[-2 * 251:])
            self.date = deepcopy(self.maxDate[-2 * 251:])
            self.prices = deepcopy(self.maxPrice[-2 * 251:])
            for i in range(len(self.original)):
                self.original[i][0] = i + 1
        if(self.level == 3): #3rd level is 1 year ago
            self.original = deepcopy(self.max[-251:])
            self.date = deepcopy(self.maxDate[-251:])
            self.prices = deepcopy(self.maxPrice[-251:])
            for i in range(len(self.original)):
                self.original[i][0] = i + 1
        if(self.level ==4): #4th level is 6 months ago
            self.original = deepcopy(self.max[-24 * 5:])
            self.date = deepcopy(self.maxDate[-24 * 5:])
            self.prices = deepcopy(self.maxPrice[-24 * 5:])
            print(self.date)
            for i in range(len(self.original)):
                self.original[i][0] = i + 1
        if(self.level == 5): #5th level is 3 months ago
            self.original = deepcopy(self.max[-12 * 5:])
            self.date = deepcopy(self.maxDate[-12 * 5:])
            self.prices = deepcopy(self.maxPrice[-12 * 5:])
            print(self.date)
            for i in range(len(self.original)):
                self.original[i][0] = i + 1
        if(self.level == 6): #6th level is 1 month ago
            self.original = deepcopy(self.max[-4*5:])
            self.date = deepcopy(self.maxDate[-4*5:])
            self.prices = deepcopy(self.maxPrice[-4 * 5:])
            print(self.date)
            for i in range(len(self.original)):
                self.original[i][0] = i + 1
        if(self.level == 7): #7th level is 1 week (5 days)
            self.original = deepcopy(self.max[-5:])
            self.date = deepcopy(self.maxDate[-5:])
            self.prices = deepcopy(self.maxPrice[-5:])
            print(self.date)
            for i in range(len(self.original)):
                self.original[i][0] = i + 1

    def userScaling(self, dateA, dateB): #user defines the range
            pass






