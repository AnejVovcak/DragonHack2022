import cv2
import time
import imutils
import numpy as np

data = {}

backgroundIteration = 10


def izpis():
    global data
    return data

def getColor(colorIndex):
    colors = {

        0 : (0,255,255), #"#FFFF00",
        1 : (0,255,0), #"#00ff00",
        2 : (0,0,255), #"#0000ff",
        3 : (255,0,0), #"#ff0000"
        4 : (0,0,0) 
    }

    return colors[colorIndex]

def RGB2HEX(color):
    return '#'+hex((color[0] << 16) + (color[1] << 8) + (color[2])).upper()[2:]

def colorDetection(frame):
    global data
    data = {}



    colorRanges = [
        [(16,68,112),(33,227,247)], #yellow
        [(40,68,112),(56,227,247)], #green
        [(0,88,0),(12,255,255)], #red
        [(81,51,0),(112,255,255)], #blue
        [(0,0,0),(179,255,14)] #black
        ]
    
    original = frame.copy()
    obj = 0
    for colorIndex,colorRange in enumerate(colorRanges):

        frame = original.copy()
        frame = cv2.GaussianBlur(frame,(9,9),0)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        frame = cv2.erode(frame, None)
        frame = cv2.dilate(frame, None)
        frame = cv2.inRange(frame,colorRange[0],colorRange[1])
        centers = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(centers)


        if len(cnts) > 0:           
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x = int(x)
                y = int(y)
                color = getColor(colorIndex)
                
                if radius > 15:
                    cv2.circle(original, (int(x), int(y)), int(radius),(int(color[0]),int(color[1]),int(color[2])), 2)
                    cv2.putText(original, str(obj)+' : ' + str(Vrsta(color,radius)) + ' : ' + str(color), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    data[str(obj)] = {
                        "x" : int(x),
                        "y" : int(y),
                        "barva" :  RGB2HEX(color[::-1]),
                        "type" : Vrsta(color,radius)
                    }
                    obj+=1
                    #cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    #print(data)
    return original


def Vrsta(color,radius):
    
    blueUpper = (162, 176, 12)
    blueLower= (84, 0, 27)
   
    if radius < 30:
        return 0
    else:
        return 1


def Mask(frame,ozadje):
    original = frame.copy()
    
    # Remove background algorithm
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = abs(ozadje-frame)
    #frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

    
    frame = cv2.GaussianBlur(frame,(19,19),0)
    ret3,frame = cv2.threshold(frame,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    cv2.imshow("frame",frame)
    """
    frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    frame = cv2.inRange(frame,(0,87,94),(179,222,150))
    cv2.imshow("frame2",frame)
"""
    #contours,_ = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (255),-1)
    frame = cv2.bitwise_and(original,original,mask=frame)
    return frame


ozadje = None
def zaznavanje():

   
    cameraFeed = cv2.VideoCapture(0)
    #cameraFeed = cv2.VideoCapture("output.avi")
    time.sleep(1)
    global ozadje
    
    for _ in range(backgroundIteration):
        ret,frame = cameraFeed.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if ozadje is None:
            ozadje = frame
        else:
            ozadje = cv2.addWeighted(frame,0.5,ozadje,0.5,0)

    
    while True:


        ret,frame = cameraFeed.read()
        if frame is None:
            break


        
        # cv2.imshow("Raw",frame);
        # masked = Mask(frame,ozadje)
        # cv2.imshow("Masked",masked);
        frame = colorDetection(frame)
        #cv2.imshow("Konec",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #print(Izpis())
    
    cameraFeed.release()
    cv2.destroyAllWindows()

#if __name__ == "__main__":
#    zaznavanje()
