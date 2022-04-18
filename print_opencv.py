# pip install mediapipe opencv-python
import cv2
from cvzone.PoseModule import PoseDetector
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import math
import numpy as np
# import mySerial

# 2 sec delay, try to reduce it(get camera with higher fps, OVERCLOCKING and maybe belh nfmhyjfjyfyujhmow)
# https://google.github.io/mediapipe/solutions/pose.html make model_complexity lower
# make sure STOP, START & PIC send once in 3.3 seconds
# new measurements for graph with hips 

video=cv2.VideoCapture(0)
video.set(3, 1280)
video.set(4, 720)

# detector_hand = HandDetector(detectionCon=0.8, maxHands=1)
# detector_pose = PoseDetector(detectionCon=0.8)


length = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57] #distance of palm->hips
z = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] #depth
coff = np.polyfit(length, z, 2)

# def getEuclideanDistance(x1,x2,y1,y2):
#     return int(math.sqrt((y2-y1)**2+(x2-x1)**2))

# def getX_Cordinate(leftHipCordinates, rightHipCordinates):
#     [index1, x1, y1, z1_inaccurate] =  leftHipCordinates 
#     [index2, x2, y2, z2_inaccurate] =  rightHipCordinates
#     x_cordinates = (x1+x2)/2 
#     return x_cordinates

# def getZ_Cordinate(leftHipCordinates, rightHipCordinates):
#     [index1, x1, y1, z1_inaccurate] =  leftHipCordinates 
#     [index2, x2, y2, z2_inaccurate] =  rightHipCordinates
#     distance = getEuclideanDistance(x1,x2,y1,y2)
#     A, B, C = coff #Ax^2+Bx+C
    
#     z_cordinates = A*distance**2 + B*distance + C
#     return z_cordinates

# def countFingers(myHand):
#     totalMatrix = detector_hand.fingersUp(myHand)
#     total=np.count_nonzero(np.array(totalMatrix))
#     return (total, myHand["type"])

while video.isOpened(): 
    ret,image=video.read()
    print("in loop")
    # hands = detector_hand.findHands(image, draw=False)
    # pose = detector_pose.findPose(image)
    # PoseLmList, bboxInfo = detector_pose.findPosition(pose)

    # position=0
    # if len(PoseLmList):
    #     x_cordinates = getX_Cordinate(PoseLmList[23], PoseLmList[24])
    #     z_cordinates = getZ_Cordinate(PoseLmList[23], PoseLmList[24])

    #     # go in reverse if less than 3.5 feet
    #     # move forward if more than 5.5 feet

    #     image_x, image_y, width, height = bboxInfo['bbox']
    #     x, y = bboxInfo['center']

    #     # mySerial.send(f"z:{int(z_cordinates)}")
    #     # mySerial.send(f"x {int(x_cordinates)}\n")

    #     cvzone.putTextRect(image, f"z: {int(z_cordinates)} cm", (x+5,y-160))
    #     cvzone.putTextRect(image, f"x: {int(x_cordinates)} cm", (x+5,y-220))
    #     cv2.rectangle(image,(x,y),(x+width,y+height),(255,0,255),3)
       
        
    #     if hands:
    #         fingersHeldUp1, hand1 = countFingers(hands[0])
    #         try:
    #             fingersHeldUp2, hand2 = countFingers(hands[1]) 
    #             numberOfHands = 2
    #         except IndexError:
    #             numberOfHands = 1
    #         [index1, LEFT_ELBOW_X, LEFT_ELBOW_Y, z1_inaccurate] =  PoseLmList[13]
    #         [index2, LEFT_WRIST_X, LEFT_WRIST_Y, z2_inaccurate] =  PoseLmList[15]
    #         [index1, RIGHT_ELBOW_X, RIGHT_ELBOW_Y, z1_inaccurate] =  PoseLmList[14]
    #         [index2, RIGHT_WRIST_X, RIGHT_WRIST_Y, z2_inaccurate] =  PoseLmList[16]
    #         isHandUp = False

    #         if (RIGHT_WRIST_Y<=RIGHT_ELBOW_Y and hand1=="Right") :
    #             isHandUp = True
    #             fingersHeldUp = fingersHeldUp1
    #         elif (LEFT_WRIST_Y<=LEFT_ELBOW_Y and hand1=="Left") :
    #             isHandUp = True
    #             fingersHeldUp = fingersHeldUp1
    #         if numberOfHands == 2:
    #             if (RIGHT_WRIST_Y<=RIGHT_ELBOW_Y and hand2=="Right") :
    #                 isHandUp = True
    #                 fingersHeldUp = fingersHeldUp2
    #             elif (LEFT_WRIST_Y<=LEFT_ELBOW_Y and hand2=="Left") :
    #                 isHandUp = True
    #                 fingersHeldUp = fingersHeldUp2
  

    #         if  (fingersHeldUp==0 or fingersHeldUp==1) and isHandUp:
    #             # mySerial.send(f"motion:move\n")
    #             print("Start Moving")
    #         elif (fingersHeldUp==2 or fingersHeldUp==3) and isHandUp:
    #             # mySerial.send(f"motion:pict\n")
    #             print("Take pICTURE")             
    #         elif (fingersHeldUp==4 or fingersHeldUp==5) and isHandUp:
    #             # mySerial.send(f"motion:stop\n")
    #             print("STOP")             

    cv2.imshow("Frame",image)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
