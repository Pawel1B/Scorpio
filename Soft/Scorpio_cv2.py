import numpy as np
import cv2

img=[]
result=[]
mask=[]
gray=[]
circle=[]
detected_circles=[]
gray_1=[]
a=[]
for i in range(1,10):
    img.append(i)
    result.append(i)
    mask.append(i)
    gray.append(i)
    circle.append(i)
    detected_circles.append(i)
    gray_1.append(i)
    a.append(i)

img[1]=cv2.imread('img/1.jpg')
img[2]=cv2.imread('img/2.jpg')
img[3]=cv2.imread('img/3.jpg')
img[4]=cv2.imread('img/4.jpg')
img[5]=cv2.imread('img/5.jpg')
img[6]=cv2.imread('img/6.jpg')
img[7]=cv2.imread('img/7.jpg')
img[8]=cv2.imread('img/8.jpg')

l_b = np.array([30,56,62])# 67,175,0
u_b = np.array([65,255,255])# 255,255,80
l_b1=np.array([0,155,0])
u_b1=np.array([255,255,255])
    
for i in range(1,9):
    (hight, width, deepth)=(img[i]).shape
    maksymalne=round(min([width,hight])/2)
    minimalny=round(max([width,hight])/10)
    hsv = cv2.cvtColor(img[i],cv2.COLOR_BGR2HSV_FULL)
    mask[i] = cv2.inRange(hsv,l_b,u_b)
    result[i]=cv2.bitwise_and(img[i],img[i],mask=mask[i])

    mask[i]=cv2.inRange(cv2.cvtColor(img[i],cv2.COLOR_BGR2RGB),l_b1,u_b1)
    result[i]=cv2.bitwise_and(result[i],result[i],mask=mask[i])

    gray[i]=cv2.cvtColor(result[i],cv2.COLOR_BGR2GRAY)
    _,mask[i] = cv2.threshold(gray[i],60,255,cv2.THRESH_BINARY)
    mask[i] = cv2.morphologyEx(mask[i], cv2.MORPH_OPEN,kernel=np.ones((12,12),np.uint8))
    mask[i] = cv2.morphologyEx(mask[i], cv2.MORPH_DILATE,kernel=np.ones((12,12),np.uint8))
    mask[i] = cv2.morphologyEx(mask[i], cv2.MORPH_CLOSE,kernel=np.ones((200,200),np.uint8))
    gray[i]=cv2.bitwise_and(gray[i],gray[i],mask=mask[i])



    circle[i]=cv2.HoughCircles(gray[i],cv2.HOUGH_GRADIENT, 1.5, minDist=minimalny,param1=200,
                        param2=31,minRadius=5,maxRadius=maksymalne)
    
    detected_circles[i]=np.uint16(np.around(circle[i]))

    marker=0
    marker_1=0
    dynamiczny_promień=0
    time=0
    for x in range(0,(hight-1)):
        if sum(gray[i][x,:])==0 and marker==0:
            marker=0
            marker_1=x
        if sum(gray[i][x,:])>0 and marker==0:
            marker=1
            marker_1=x
        if sum(gray[i][x,:])==0 and marker==1:
            marker=0
            dynamiczny_promień=x-marker_1
            if time==0:
                time=dynamiczny_promień
            if time!=0 and time >=dynamiczny_promień:
                time=dynamiczny_promień

    promień_1=round(time/2)
    marker=0
    marker_1=0
    dynamiczny_promień=0
    time=0
    for y in range(0,(width-1)):
        if sum(gray[i][:,y])==0 and marker==0:
            marker=0
            marker_1=y
        if sum(gray[i][:,y])>0 and marker==0:
            marker=1
            marker_1=y
        if sum(gray[i][:,y])==0 and marker==1:
            marker=0
            dynamiczny_promień=y-marker_1
            if time==0:
                time=dynamiczny_promień
            if time!=0 and time >=dynamiczny_promień:
                time=dynamiczny_promień

    promień_2=round(time/2)

    gray_1[i]=gray[i].copy()

    promień_min=min(promień_1,promień_2)
    promień_max=max(promień_1,promień_2)
    mem_1,mem_2,mem_3=0,0,0
    print('Zdjęcie numer: ',i)
    for (x,y,r) in detected_circles[i][0,:]:
        if  x>width or y>hight or (r>1.15*promień_max or r<0.90*promień_min) or mem_1!=0 and ((gray_1[i][y,x]==(0,255,0)).any() and ((mem_2+mem_3)<(y+r) and ((mem_1+mem_3)>(x-r) or (mem_1-mem_3)<(x+r)) or  ((mem_2+mem_3)<(y-r) and ((mem_1+mem_3)>(x-r) or (mem_1-mem_3)<(x+r)))) ) :
            x=0
            y=0
            r=0
        if r>0:
            cv2.circle(img[i],(x,y),r,(0,255,0),-1)
            cv2.circle(gray_1[i],(x,y),r,(0,255,0),-1)
            mem_1,mem_2,mem_3=x,y,r
            strxy = str(x)+','+str(y)
            cv2.putText(img[i],strxy,(x,y),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),2)
            print('X= ',x,'Y= ',y)
    cv2.imshow('result'+str(i),img[i])
cv2.waitKey(0)
cv2.destroyAllWindows()