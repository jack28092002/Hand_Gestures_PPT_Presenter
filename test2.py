import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#Variables
width,height=720,360
folderPath="Presentation"

#Camera setup
cap =cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#get the list of presentation images
pathImages=sorted(os.listdir(folderPath),key=len)
print(pathImages)

#variables
imgNumber=0
hs,ws=int(120*1),int(213*1)
gestureThreshold=170
buttonPressed=False
buttonCounter=0
buttonDelay=30


# Hand Detector
detector=HandDetector(detectionCon=0.8,maxHands=1)
while True:
    #Import Images
    success,img=cap.read()
    img=cv2.flip(img,1)
    pathFullImage=os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent=cv2.imread(pathFullImage)
    
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)



    if hands and buttonPressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        # indexFinger = hand['lmList'][8][0], hand['lmList'][8][1] 
        # (lmlist=hand['lmlist']
        # indexFinger=lmlist[8][0],lmlist[8][1]

        #Gesture 1- Left
        if fingers==[1,0,0,0,0]:
                print("Left")
                buttonPressed=True
                imgNumber-=1
                if imgNumber<0:
                    imgNumber=0
        
        #Gesture 2- Right
        if fingers==[0,0,0,0,1]:
                print("Right")
                buttonPressed=True
                imgNumber+=1
                if imgNumber>len(pathImages)-1:
                    imgNumber=len(pathImages)-1
        
        #Gesture 3- close
        if fingers==[0,0,0,1,0]:
                print("Close")
                buttonPressed=True 
                cv2.destroyAllWindows()
                break
        #Gesture 4 -Show pointer
        if fingers == [0, 1, 1, 0, 0]:  # Show Pointer (index and middle fingers extended)
                print("Show Pointer")
                try:
                        indexFinger = hand['lmList'][8][0], hand['lmList'][8][1]  # Index finger landmark
                       
                        cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)  # Draw a filled circle (red pointer)
                except IndexError:
                    print("Error: Unable to access hand landmarks.")
            




    # Button Pressed Iterations
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter>buttonDelay: 
            buttonCounter=0
            buttonPressed=False
        
    #Adding webcam image on the sides
    imgSmall=cv2.resize(img,(ws,hs))
    h,w,_=imgCurrent.shape
    imgCurrent[0:hs,0:ws]=imgSmall


    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)

    key=cv2.waitKey(1)
    if key==ord('q'):
        break
