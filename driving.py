from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
import numpy as np
from pynput.keyboard import Key,Controller
keyboard=Controller()
cords = [(10,20,177,120,'ur'),(177,20,343,120,'u'),(343,20,510,120,'ul'),(10,120,177,220,'r'),(177,120,343,220,''),(343,120,510,220,'l'),(10,220,177,320,'dr'),(177,220,343,320,'d'),(343,220,510,320,'dl')]
gearCheckReverse = False
gearCheckAuto = False
gearReverse = False

cap = cv2.VideoCapture(0)
detection_graph, sess = detector_utils.load_inference_graph() 

def Drive(a,b,x,y):
    global gearReverse, gearCheck
    if b - y > 40:
        keyboard.press('d')
        keyboard.release('w')
    elif b - y < -40:
        keyboard.press('a')
        keyboard.release('w')
    elif b - y > -40 and b - y < 40:
        keyboard.release('d')
        keyboard.release('a')
        if gearReverse:
            keyboard.release('w')
            keyboard.press('s')
        else:
            keyboard.release('s')
            keyboard.press('w')
        
def controls(x,y):
    global gearReverse, gearCheckReverse, gearCheckAuto
    l=len(cords)
    for i in range(l):
        tuple = cords[i]
        x1=tuple[0]
        y1=tuple[1]
        x2=tuple[2]
        y2=tuple[3]
        inp=tuple[4]
		
        if x>x1 and x<x2 and y>y1 and y<y2 :
            if inp == 'ur' and not gearReverse:
                gearCheckReverse=True
            elif inp == 'dr' and gearCheckReverse:
                gearCheckReverse=False
                gearReverse=True
            if inp == 'dr' and gearReverse:
                gearCheckAuto=True
            elif inp == 'ur' and gearCheckAuto:
                gearCheckAuto=False
                gearReverse=False
            print(gearReverse)
            print(inp)
            break

def Steering(img,dime):
    check1=False
    check2=False
    
    if len(dime)<2:
        return img
    	
    if len(dime)<4:
        A=dime[0]
        B=dime[1]
        cv2.circle(img, (A,B),2,(0,0,255),2)
        print("Controls")
        controls(A,B)
        return img
    	
    A=dime[0]
    B=dime[1]
    	
    if A < 260 :
        cv2.circle(img, (A,B),2,(0,0,255),2)
        Ax_axis = A
        By_axis = B
        check1=True
    else:
        cv2.circle(img, (A,B),2,(0,255,0),2)
        Xx_axis = A
        Yy_axis = B
        check2=True
    
    X=dime[2]
    Y=dime[3]
    
    cv2.circle(img, (X,Y),2,(0,255,0),2)
    if X < 260 :
        cv2.circle(img, (X,Y),2,(0,0,255),2)
        Ax_axis = X
        By_axis = Y
        check1=True
    else:
        cv2.circle(img, (X,Y),2,(0,255,0),2)
        Xx_axis = X
        Yy_axis = Y

        check2=True
    if check1 and check2:
        print("Drive")
        Drive(Ax_axis,By_axis,Xx_axis,Yy_axis)
    return img

if __name__ == '__main__':
    im_width, im_height = (cap.get(3), cap.get(4))
    num_hands_detect=2
    cv2.namedWindow('Hand Gesture Detection', cv2.WINDOW_NORMAL)

    while True:
        ret, image_np = cap.read()
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        boxes, scores = detector_utils.detect_objects(
            image_np, detection_graph, sess)

        lst=detector_utils.draw_box_on_image(
            num_hands_detect, 0.2, scores, boxes, im_width, im_height, image_np)
        Steering(image_np,lst)
        print(lst)
        image_np = cv2.flip(image_np,1)
        cv2.imshow('Single-Threaded Detection', cv2.cvtColor(
    	    image_np, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
