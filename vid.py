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

def RGB2HEX(colorIndex):
    colors = {
        0 : "#FFFF00",
        1 : "#00FF00",
        2 : "#FF0000",
        3 : "#0000FF",
        4 : "#000000"
    }
    return colors[colorIndex]

def Vrsta(colorIndex):
    
    if colorIndex<2:
        return 2
    elif colorIndex<4:
        return 1
    return 0


def grabCenters(frame,colorRange):
    
    frame = cv2.GaussianBlur(frame,(9,9),0)  #Izniči šum
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # Pretvori v HSV vrednosti
    frame = cv2.erode(frame, None) #Pomanjšaj in povečaj da še bolj izničiš šum
    frame = cv2.dilate(frame, None) 
    frame = cv2.inRange(frame,colorRange[0],colorRange[1]) #Ustvari masko glede na vrednosti posameznih pikslov


    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    frame = cv2.erode(frame,element)
    
    centers = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #najdi posamezne dele ki jih maska ne pokriva
    cnts = imutils.grab_contours(centers) #pretvori posamezne dele v array
    return cnts



def colorDetection(frame):
    global data

    newdata = {}

    """    #Array mejnih vrednosti posameznih barv
    colorRanges = [
        [(16,68,112),(33,227,247)], #yellow
        [(40,68,112),(56,227,247)], #green
        [(0,88,127),(12,255,255)], #red
        [(81,51,0),(112,255,255)], #blue
        [(0,0,223),(168,41,255)] #black
        ]
   """
    

    colorRanges = [
        [(28,106,64),(43,255,255)], #yellow
        [(46,71,127),(78,210,241)], #green
        [(151,106,64),(179,255,255)], #red
        [(65,106,64),(113,255,255)], #blue
        [(98,56,101),(113,103,125)] #black
        ]
    
    original = frame.copy()
    objId = 0

    for colorIndex,colorRange in enumerate(colorRanges):   #Za vsako barvo

        cnts = grabCenters(original.copy(),colorRange) #Poišči centre najdenih delov

                   
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c) #najmanjši očrtani krog okoli najdenih delov
            x = int(x)
            y = int(y)

            color = getColor(colorIndex)  #Barva balinčka
                
            if radius > 30 or (colorIndex == 4 and radius >10):
                cv2.circle(original, (int(x), int(y)), int(radius),(int(color[0]),int(color[1]),int(color[2])), 2)
                cv2.putText(original, str(colorIndex)+' : ' + str(Vrsta(colorIndex)), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                
                newdata[str(objId)] = {
                    "x" : x,  #X koordinata
                    "y" : y, #Y koordinata
                    "barva" :  RGB2HEX(colorIndex), #Barva balinčka                #Zapiši podatke v dictionary za na server
                    "type" : Vrsta(colorIndex) #Ekipa balinčka
                }
                
                objId+=1

    data = newdata
    return original



def zaznavanje():
    cameraFeed = cv2.VideoCapture(0)

    time.sleep(1) #Čakaj da se kamera gotovo poveže
    while True:


        ret,frame = cameraFeed.read()  #Beri frame iz streama in preveri uspešnost branja
        while frame is None:
            break
        
        frame = colorDetection(frame) #Zaznaj objekte

        #cv2.imshow("Frame",frame) #Prikaži zaznane objekte na sliki (Zakomentirano za rPi)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cameraFeed.release() #Sprosti procese in zapri odprta okna
    cv2.destroyAllWindows() 

#if __name__ == "__main__":
#    zaznavanje()
