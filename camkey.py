import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8,maxHands=1)
finalText =""
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",":"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

def drawALL(img,buttonList):
    for button in buttonList:
        x,y= button.pos
        w, h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img

class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text = text
        self.size = size
       

buttonList = []
for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            buttonList.append(Button([100*j+50,100*i+50],key))


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img=drawALL(img,buttonList)
    if hands:
        hand1=hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        for button in buttonList:
            x, y = button.pos
            w, h= button.size
            if x< lmList1[8][0]<x+w and y< lmList1[8][1]<y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,0),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                l,_,_=detector.findDistance(lmList1[8],lmList1[12],img)
                #print(l)

                if l<30:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,255),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    finalText += button.text 
                    sleep(0.2)

    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60,425),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
    cv2.imshow("Image",img)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break

img.release()
cv2.destroyAllWindows()
