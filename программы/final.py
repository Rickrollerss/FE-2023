import cv2
import RobotAPI as rapi
import numpy as np
import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate=115200, stopbits=serial.STOPBITS_ONE)
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

message = ""
fps = 0
fps1 = 0
fps_time = 0

xb11, yb11 = 0, 290
xb21, yb21 = 140, 320

xb12, yb12 = 500, 290
xb22, yb22 = 640, 320


xz1, yz1 = 140, 200
xz2, yz2 = 500, 390

xp1, yp1 = 300, 400
xp2, yp2 = 340, 430

lowb=np.array([0,0,0])
upb=np.array([180,255,50])


lowbl=np.array([90,100,50])
upbl=np.array([120,255,255])


lowor=np.array([0,100,50])
upor=np.array([30,255,255])

lowred=np.array([0,100,50])
upred=np.array([6,255,255])

lowgreen=np.array([72,200,38])
upgreen=np.array([83,255,166])

e_old = 0
dat1 = 0
dat2 = 0
dat1_old = 0
dat2_old = 0
timerd1 = time.time()
timerd2 = time.time()

deg = 0
speed = 0
color = 6
inn = ""
line = 'none'
direction = 'none'

znak1 = 'none'
per = 0
time_per = time.time()
timer_b = time.time()
timer_stop = time.time()


def black_line():
    global xb11, yb11, xb21, yb21, xb12, yb12, xb22, yb22, lowb, upb, dat1, dat2,timerd1,timerd2,dat1_old,dat2_old
    datb1 = frame[yb11:yb21, xb11:xb21]
    hsv1 = cv2.cvtColor(datb1, cv2.COLOR_BGR2HSV)
    maskd1 = cv2.inRange(hsv1, lowb, upb)
    gray = cv2.cvtColor(maskd1, cv2.COLOR_GRAY2BGR)
    frame[yb11:yb21, xb11:xb21] = gray

    imd1, contoursd1, hod1 = cv2.findContours(maskd1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    dat1 = 0
    x1, y1, w1, h1 = 0,0,0,0
    for contorb1 in contoursd1:
        x, y, w, h = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 150 and x1 + w1 < x + w and a1/w*h>0.5:
            x1, y1, w1, h1 = x, y, w, h
    cv2.rectangle(datb1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    dat1 = int(100*(x1 + w1)/(xb21-xb11))
    if dat1 > 0:
        dat1_old = dat1
        timerd1 = time.time()
    else:
        if timerd1 + 0.05 > time.time():
            dat1 = dat1_old






    datb2 = frame[yb12:yb22, xb12:xb22]
    hsv2 = cv2.cvtColor(datb2, cv2.COLOR_BGR2HSV)
    maskd2 = cv2.inRange(hsv2, lowb, upb)
    gray = cv2.cvtColor(maskd2, cv2.COLOR_GRAY2BGR)
    frame[yb12:yb22, xb12:xb22] = gray

    imd2, contoursd2, hod2 = cv2.findContours(maskd2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    dat2 = 0
    x2, y2, w2, h2 = xb22 - xb12, 0, 0, 0
    for contorb2 in contoursd2:
        x, y, w, h = cv2.boundingRect(contorb2)
        a1 = cv2.contourArea(contorb2)
        if a1 > 150 and (xb22 - xb12) - x2 < (xb22 - xb12) - x and a1/w*h>0.5:
            x2, y2, w2, h2 = x, y, w, h
    cv2.rectangle(datb2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
    dat2 = int(100 * ((xb22 - xb12) - x2) / (xb22 - xb12))
    if dat2 > 0:
        dat2_old = dat2
        timerd2 = time.time()
    else:
        if timerd2 + 0.05 > time.time():
            dat2 = dat2_old

def znak():
    global xz1, yz1, xz2, yz2,znak1
    znak1 ="none"
    dat = frame[yz1:yz2, xz1:xz2]
    cv2.rectangle(frame, (xz1, yz1), (xz2, yz2), (0, 255, 0), 2)
    hsv = cv2.cvtColor(dat, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lowred, upred)
    imd, contours, hod = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    x2, y2, w2, h2 = 0, 0, 0, 0
    for contor in contours:
        x, y, w, h = cv2.boundingRect(contor)
        a1 = cv2.contourArea(contor)
        if a1 > 50 and w2 * h2 < w * h:
            x2, y2, w2, h2 = x, y, w, h
            znak1 = 'red'
    cv2.rectangle(dat, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)
    mask2 = cv2.inRange(hsv, lowgreen, upgreen)
    imd, contours, hod = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    x2, y2, w2, h2 = 0, 0, 0, 0
    for contor in contours:
        x, y, w, h = cv2.boundingRect(contor)
        a1 = cv2.contourArea(contor)
        if a1 > 50 and w2 * h2 < w * h:
            x2, y2, w2, h2 = x, y, w, h
            znak1 = 'red'
    cv2.rectangle(dat, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)



def povorot():
    global xp1, yp1, xp2, yp2, line, direction, per, time_per, color
    dat = frame[yp1:yp2, xp1:xp2]
    cv2.rectangle(frame, (xp1, yp1), (xp2, yp2), (0, 255, 0), 2)
    hsv = cv2.cvtColor(dat, cv2.COLOR_BGR2HSV)
    line = 'none'

    if direction == 'none':
        mask = cv2.inRange(hsv, lowbl, upbl)
        imd, contours, hod = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x1, y1, w1, h1 = 0, 0, 0, 0
        for contor in contours:
            x, y, w, h = cv2.boundingRect(contor)
            a1 = cv2.contourArea(contor)
            if a1 > 50 and w1 * h1 < w * h:
                x1, y1, w1, h1 = x, y, w, h
                line = 'blue'
        cv2.rectangle(dat, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)

        mask = cv2.inRange(hsv, lowor, upor)
        imd, contours, hod = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x2, y2, w2, h2 = 0, 0, 0, 0
        for contor in contours:
            x, y, w, h = cv2.boundingRect(contor)
            a1 = cv2.contourArea(contor)
            if a1 > 50 and w2 * h2 < w * h:
                x2, y2, w2, h2 = x, y, w, h
                line = 'orange'
        cv2.rectangle(dat, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)
        direction = line
        per = 1
        time_per = time.time()
    else:
        if direction == 'blue':
            mask = cv2.inRange(hsv, lowbl, upbl)
            imd, contours, hod = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            x1, y1, w1, h1 = 0, 0, 0, 0
            for contor in contours:
                x, y, w, h = cv2.boundingRect(contor)
                a1 = cv2.contourArea(contor)
                if a1 > 50 and w1 * h1 < w * h:
                    x1, y1, w1, h1 = x, y, w, h
                    line = 'blue'
            cv2.rectangle(dat, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            if line == 'blue' and time_per + 0.5 < time.time():
                time_per = time.time()
                per += 1
                color = 2

        if direction == 'orange':
            mask = cv2.inRange(hsv, lowor, upor)
            imd, contours, hod = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            x2, y2, w2, h2 = 0, 0, 0, 0
            for contor in contours:
                x, y, w, h = cv2.boundingRect(contor)
                a1 = cv2.contourArea(contor)
                if a1 > 50 and w2 * h2 < w * h:
                    x2, y2, w2, h2 = x, y, w, h
                    line = 'orange'
            cv2.rectangle(dat, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)
            if line == 'orange' and time_per + 0.5 < time.time():
                time_per = time.time()
                per += 1
                color = 4



def pd():
    global  e_old,dat2,dat1
    kp = 0.4
    kd = 0.4
    u = 0
    if dat2>0 and dat1>0:
        e = dat2 - dat1
        if e>-2 and e<2: e = 0

        u = e * kp + (e - e_old) * kd
        e_old = e
        if u > 90: u = 90
        if u < -90: u = -90
    else:
        if dat2 == 0 and dat1 == 0:
            if direction == 'orange':
                u = -90
            if direction == 'blue':
                u = 90
        else:
            if dat2 == 0:
                u = 25
            if dat1 == 0:
                u = -25

    return -u



while 1:
    frame = robot.get_frame(wait_new_frame=1)
    if speed > 0:
        black_line()
        znak()
        povorot()
        deg = pd()
    else:
        black_line()
        znak()
        povorot()
        deg = 0



    if per == 12:
        if timer_stop + 1.4 < time.time():
            speed = 0
    else:
        timer_stop = time.time()

    message = str(int(speed) + 500) + str(int(deg) + 500) + str(int(color)) +'$'
    port.write(message.encode("utf-8"))

    if port.in_waiting > 0:
        inn = ""
        t = time.time()
        while 1:
            a = str(port.read(), "utf-8")
            if a != '$':
                inn += a
            else:
                break
            if t + 0.02 < time.time():
                break
        port.reset_input_buffer()


    if inn == '0' and timer_b + 1 < time.time():
        timer_b = time.time()
        if speed == 0:
            speed = 100
        else:
            speed = 0


    cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
    cv2.rectangle(frame, (xb11, yb11), (xb21, yb21), (0, 0, 255), 2)
    cv2.rectangle(frame, (xb12, yb12), (xb22, yb22), (0, 0, 255), 2)

    robot.text_to_frame(frame, message, 0, 20)
    robot.text_to_frame(frame, direction, 150, 20)
    robot.text_to_frame(frame, line, 300, 20)
    robot.text_to_frame(frame, znak1, 300, 40)
    robot.text_to_frame(frame, inn, 0, 40)
    robot.text_to_frame(frame, str(dat1) + '  ' + str(dat2), 0, 60)

    fps1 += 1
    if time.time() > fps_time + 1:
        fps_time = time.time()
        fps = fps1
        fps1 = 0

    robot.text_to_frame(frame, 'fps = ' + str(fps), 500, 20)
    robot.text_to_frame(frame, 'per = ' + str(per), 500, 40)
    robot.set_frame(frame, 40)