# pip install mediapipe opencv-python
import cv2
import mediapipe as mp
import time
# import mySerial

# The x axis controls the steering and the z axis controls distance between the travelBot and the person
# x axis ranges from 0 to 1. 0 is right facing travelBot, travelBot should steer left. 1 is left facing the bot, bot should steer right.(normalize values to range(-1,1))
# z axis ranges from -2 to 0. -2 is the closest distance to the bot and 0 is far away.
# bot should keep a distance of -0.5 with some allowance on z axis(value has not been normalized) 
# tracking average of right hip and left hip

mp_draw=mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic
tipIds=[3,8,12,16,20]

video=cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4, model_complexity=1 ) as holistic:
    while video.isOpened():
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=holistic.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        hand_lmList=[]

        if results.right_hand_landmarks:    
            hand="right"      
            myHands=results.right_hand_landmarks
            for hand_id, hand_lm in enumerate(myHands.landmark):
                h,w,c=image.shape
                cx,cy= int(hand_lm.x*w), int(hand_lm.y*h)
                hand_lmList.append([hand_id,cx,cy])
            mp_draw.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        elif results.left_hand_landmarks: 
            hand="left"         
            myHands=results.left_hand_landmarks
            for hand_id, hand_lm in enumerate(myHands.landmark):
                h,w,c=image.shape
                cx,cy= int(hand_lm.x*w), int(hand_lm.y*h)
                hand_lmList.append([hand_id,cx,cy])
            mp_draw.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        else :
            hand=""

        fingers=[]
        if len(hand_lmList)!=0:
            if hand_lmList[tipIds[0]][1] > hand_lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for hand_id in range(1,5):
                if hand_lmList[tipIds[hand_id]][2] < hand_lmList[tipIds[hand_id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)

            try: 
                pose_landmarks = results.pose_landmarks.landmark
                LEFT_ELBOW=pose_landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value]
                LEFT_WRIST=pose_landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value]

                RIGHT_ELBOW=pose_landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value]
                RIGHT_WRIST=pose_landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value]


                # print(f"RIGHT_WRIST.x: {RIGHT_WRIST.x}")
                print(f"RIGHT_WRIST.z: {RIGHT_WRIST.z}")
                if ( (RIGHT_WRIST.y<=RIGHT_ELBOW.y and hand=="right") or (LEFT_WRIST.y<=LEFT_ELBOW.y and hand=="left") ) :
                    isHandUp = True
                else :
                    isHandUp = False
            except:
                isHandUp = False
                pass 
            mp_draw.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
  
            #if (isHandUp) : 
                # print(total)  send over UART to UNO
                # if  (total==0 or total==1) : 
                #   mySerial.send("mov")
                #   time.sleep(1.5)
                # elif (total==2 or total==3) :
                #   mySerial.send("pic")
                #   time.sleep(6.5)
                # elif (total==4 or total==5) :
                #   mySerial.send("stp")
                #   time.sleep(1.5)

            if  (total==0 or total==1) and isHandUp:
                cv2.rectangle(image, (20, 300), (500, 420), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "START", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "MOVING", (250, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
            elif (total==2 or total==3) and isHandUp:
                cv2.rectangle(image, (20, 300), (500, 420), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "TAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "PICTURE", (220, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
            elif (total==5 or total==4) and isHandUp:
                cv2.rectangle(image, (20, 300), (500, 420), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "STOP", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "MOVING", (220, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()