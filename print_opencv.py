# pip install mediapipe opencv-python
import cv2
# from cvzone.PoseModule import PoseDetector
# import numpy as np
# from cvzone.HandTrackingModule import HandDetector
# import cvzone

video=cv2.VideoCapture(1)
video.set(3, 1280)
video.set(4, 720)

# detector_hand = HandDetector(detectionCon=0.8, maxHands=1)
# detector_pose = PoseDetector(detectionCon=0.8)

while True: 
    ret,image=video.read()
    print("in loop")
    # hands = detector_hand.findHands(image, draw=False)
    # pose = detector_pose.findPose(image)
    # PoseLmList, bboxInfo = detector_pose.findPosition(pose)

    cv2.imshow("Frame",image)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
