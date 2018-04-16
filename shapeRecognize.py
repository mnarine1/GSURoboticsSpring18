#Code heavily adapted from Huang Manutea on github
#link to source code: https://github.com/HUANGManutea/shapeDetection

import cv2
import numpy as np
import math

device = cv2.VideoCapture(1)
scale = 1
color = (255,0,0)
text = ''

def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)


while True:
        ret, frame = device.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        #blue
        blue_lower_range = np.array([105,100,50])
        blue_upper_range = np.array([125,255,255])
        #green
        green_lower_range = np.array([40,80,30])
        green_upper_range = np.array([80,255,255])
        #red range 1
        red_lower_range1 = np.array([0,125,50])
        red_upper_range1 = np.array([10,255,255])
        #red range 2
        red_lower_range2 = np.array([150,120,50])
        red_upper_range2 = np.array([179,255,255])

        #Filters RAW image by red, green, and blue
        bmask = cv2.inRange(hsv, blue_lower_range, blue_upper_range)
        r1mask = cv2.inRange(hsv, red_lower_range1, red_upper_range1)
        r2mask = cv2.inRange(hsv, red_lower_range2, red_upper_range2)
        rmask = cv2.bitwise_or(r1mask, r2mask)
        gmask = cv2.inRange(hsv, green_lower_range, green_upper_range)


        #Combines red, green, abd blue masks into one mask
        rb = cv2.bitwise_or(rmask, bmask)
        result = cv2.bitwise_or(rb, gmask)

        colorCom = cv2.bitwise_and(frame, frame, mask=result)

        #Displays Red, Green, and Blue objects only
        cv2.imshow("Red Green Blue",colorCom)

        bresult = cv2.bitwise_and(frame, frame, mask=bmask)
        rresult = cv2.bitwise_and(frame, frame, mask=rmask)
        gresult = cv2.bitwise_and(frame, frame, mask=gmask)

        #Combines Canny edge detection masks into one edge mask
        rgbCanny = cv2.bitwise_or(cv2.bitwise_or(cv2.Canny(rmask,89,240,3),cv2.Canny(gmask,89,240,3)),cv2.Canny(bmask,89,240,3))
        cv2.imshow("Canny", rgbCanny)


        for x in range(0,3):    #from 0 to 2
            if x==0:                #red values
                canny = cv2.Canny(rmask,89,240,3)
                color = (0,0,255)
                text = 'RED '
            elif x==1:              #green values
                canny = cv2.Canny(gmask,89,240,3)
                color = (0,255,0)
                text = 'GREEN '
            elif x==2:              #blue values
                canny = cv2.Canny(bmask,89,240,3)
                color = (255,0,0)
                text = 'BLUE '



            if ret==True:
                #contours
                canny2, contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for i in range(0,len(contours)):
                    #approximate the contour with accuracy proportional to
                    #the contour perimeter
                    approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)
                    #Skip small or non-convex objects
                    if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                        continue
                    #triangle
                    if(len(approx) == 3):
                        x,y,w,h = cv2.boundingRect(contours[i])
                        cv2.putText(frame,text + 'TRI',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,color,2,cv2.LINE_AA)
                    elif(len(approx)>=4 and len(approx)<=6):
                        #nb vertices of a polygonal curve
                        vtc = len(approx)
                        #get cos of all corners
                        cos = []
                        for j in range(2,vtc+1):
                            cos.append(angle(approx[j%vtc],approx[j-2],approx[j-1]))
                        #sort ascending cos
                        cos.sort()
                        #get lowest and highest
                        mincos = cos[0]
                        maxcos = cos[-1]

                        #Use the degrees obtained above and the number of vertices
                        #to determine the shape of the contour
                        x,y,w,h = cv2.boundingRect(contours[i])
                        if(vtc==4):
                            cv2.putText(frame,text + 'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,color,2,cv2.LINE_AA)
                    else:
                        #detect and label circle
                        area = cv2.contourArea(contours[i])
                        x,y,w,h = cv2.boundingRect(contours[i])
                        radius = w/2
                        if(abs(1 - (float(w)/h))<=2 and abs(1-(area/(math.pi*radius*radius)))<=0.2):
                            cv2.putText(frame,text + 'CIRC',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,color,2,cv2.LINE_AA)


        cv2.imshow("Frame", frame)



        if cv2.waitKey(1) == 27:
            break

device.release()
cv2.destroyAllWindows()
