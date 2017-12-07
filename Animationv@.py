# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
from Graphing import *
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.csv = Graph(data)
    data.priceInfo = []
    data.pricePosition = ()
    pass

def mousePressed(event, data):
    # use event.x and event.y
    #first
    #Hovering => how to map tkinter position to date, price data
    #price data, back solve
    date = round((event.x - data.csv.xOrigin)/data.csv.xStretch)
    price = (data.csv.yOrigin - event.y)/data.csv.yStretch + data.csv.priceOrigin
    data.priceInfo = [date, price]
    data.pricePosition = (event.x, event.y)

    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.keysym == "Up" or event.keysym == "Right"):
        data.csv.scaling(data,1)
    elif(event.keysym == "Down" or event.keysym == "Left"):
        data.csv.scaling(data,-1)
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    data.csv.draw(canvas,data)
    if len(data.priceInfo) != 0:
        canvas.create_text(data.pricePosition,
                           text = "(%s , %d)" % (data.csv.date[data.priceInfo[0]], data.priceInfo[1]), anchor = "s")
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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

run(1000, 1000)