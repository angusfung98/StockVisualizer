# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
from Profile import *
from Graphing import *
from DataScrape import *
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.entry = (data.width/2, data.height/2)#coordinates of buttons
    #profile data
    data.index = ""
    #entry fields booleans
    data.entryField = False
    #Graph info
    data.csv = None
    data.priceInfo = []
    data.position = None
    #Stock Data
    data.current = None
    data.open = None
    data.close = None

def mousePressed(event, data):
    # use event.x and event.y

    if (data.csv != None):
        if(data.csv.xOrigin<event.x<data.csv.xOrigin + 10 * data.csv.xScaling and \
           data.csv.yOrigin - 11 * data.csv.yScaling<event.y< data.csv.yOrigin ):
            data.position = round((event.x - data.csv.xOrigin) / data.csv.xStretch)
            print(data.position)
            data.pricePosition = (event.x, event.y)
    if data.width/2<event.x< data.width/2 + 100 and data.height -40 < event.y <   data.height :
        data.entryField = True
def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.keysym == "Up" or event.keysym == "Right"):
        data.csv.scaling(data,1)
    elif(event.keysym == "Down" or event.keysym == "Left"):
        data.csv.scaling(data,-1)
    if (data.entryField):
        print(event.keysym)
        if (event.keysym == "Return"):

            data.csv = Graph(data.index)
            scraping(data)
            data.entryField = False
        if (event.keysym == "BackSpace"):
            data.index = data.index[:-1]
        if (event.char.isalpha()):
            data.index +=  event.char

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height,
                            fill='AntiqueWhite1', width=0)
    if data.csv != None:
        data.csv.draw(canvas, data)
    if data.position != None:
        canvas.create_text(data.pricePosition,
                           text="(%s , %.2f)" % (data.csv.date[data.position], data.csv.prices[data.position]),
                           anchor="s")
    canvas.create_text(data.width/2,0, text = " ShiTrade", anchor = "n")
    canvas.create_text(data.width/2, data.height -20 , text = "Enter a Stock" ,anchor = 'e' )

    canvas.create_rectangle(data.width/2, data.height -40, data.width/2 + 100, data.height, fill = "white")

    canvas.create_text(data.width/2, data.height-60, text = "%s Stock History" % data.index, font = 20)
    if (data.current != None):
        canvas.create_text(data.width/4, data.height-60, text = "Current Price: %s" % (data.current), font = 20)
        canvas.create_text(3*data.width / 4, data.height - 60, text="Previous Close: %s" % (data.close), font=20)
        canvas.create_text(3*data.width/4, data.height - 30, text ="Today's Open: %.2f" % (data.csv.maxPrice[-1]),
                           font = 20)
    if (data.entryField):
        canvas.create_text(data.width/2+10, data.height-20 , text = data.index ,anchor = 'w' )


####################################
# use the run function as-is
####################################

def run(width=1000, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 500)