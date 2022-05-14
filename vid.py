import cv2
import time
import imutils
import numpy as np

data = {}

def izpis():
    global data
    return data

def RGB2HEX(color):
    return '#'+(hex(color[0])[2:].rjust(2,'0') + hex(color[1])[2:].rjust(2,'0') + hex(color[2])[2:].rjust(2,'0')).upper()

def Mask(frame):
    
    original = frame   
    frame = cv2.GaussianBlur(frame,(9,9),0)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    frame = cv2.dilate(frame, None)
    frame = cv2.erode(frame, None)
    
    frame = cv2.threshold(frame,70,255,cv2.THRESH_BINARY)[1]
    frame = cv2.bitwise_not(frame)

    return frame


def zaznavanje():
    """
    while True:
        image = cv2.imread("input.png")
        cv2.imshow("Raw",image)
        masked = Mask(image)
        cv2.imshow("Masked",image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
        
    return
    """

    #Video
    
    cameraFeed = cv2.VideoCapture(0)


    time.sleep(1)




    i = 0
    ozadje = None

    while 1:


        """
        while i<100:
            ret,frame = cameraFeed.read()
            if ozadje is None:
                ozadje = np.array(frame)
            else:
                ozadje = np.add(np.array(frame),ozadje)



            
            i+=1


        #ozadje = ozadje/100
        cv2.imshow("Ozadje",ozadje)
        print(ozadje)
        print(frame)
        return

        """

        ret,frame = cameraFeed.read()
        if frame is None:
            break
        while not ret:
            continue

        cv2.imshow("Raw",frame)
        masked = Mask(frame)
        cv2.imshow("Masked",masked)
        
        centers = cv2.findContours(masked.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(centers)
        i = 0
        global data
        data = {}
        if len(cnts) > 0:           
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x = int(x)
                y = int(y)
                color = frame[y,x]
                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(int(color[0]),int(color[1]),int(color[2])), -1)
                    data[str(i)] = {
                        "x" : int(x),
                        "y" : int(y),
                        "barva" :  RGB2HEX(color)
                    }
                    i+=1
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)

        cv2.imshow("KOnec",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cameraFeed.release()
    cv2.destroyAllWindows()

#zaznavanje()
