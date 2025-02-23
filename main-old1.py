# Bibliotheken laden
#import rp2
from time import sleep_ms, ticks_ms
from machine import I2C, Pin, Timer
from machine_i2c_lcd import I2cLcd
import _thread

# Initialisierung I2C
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=100000)

# Initialisierung LCD über I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Initialisierung von GPIO25 als Ausgang
led_onboard = Pin(25, Pin.OUT)


# Initialisierung: Button an GPIO
btn1 = Pin(9, Pin.IN, Pin.PULL_UP)
btn2 = Pin(22, Pin.IN, Pin.PULL_UP)
btn3 = Pin(14, Pin.IN, Pin.PULL_UP)
btn4 = Pin(17, Pin.IN, Pin.PULL_UP)

inppos = [0, 1, 3, 4, 6]
incre = [6000, 600, 100, 10, 1]
acdtimers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# moderun werte: 0 mode auswahl, 1 stopuhr, 2 eingabe countdown, 3 I love you, 4 countdown run
moderun = 1
modenext = 0


t1 = 0
t2 = 0
t3 = 0
t4 = 0
timecount = 0
timebtn = 0

anzcd = 0

cdtimer = 0
cdstart = 0
cdges = 0
cdpos = 0

outon = 0
outs1 = ""
outs2 = ""

mode2sub = 0
mode2run = 0





# Funktion: Blinkende LED
def blink():
    global led_onboard
    while True:
        # LED einschalten
        led_onboard.on()
        # halbe Sekunde warten
        sleep_ms(500)
        # LED ausschalten
        led_onboard.off()
        # 1 Sekunde warten
        sleep_ms(999)

def asyncout():
    global outon, outs1, outs2
    lo1 = outs1
    lo2 = outs2
    while True:
        if outon == 1:
            dummy = 1
            lcd.move_to(0, 0)
            lcd.putstr(outs1)
            lcd.move_to(0, 1)
            lcd.putstr(outs2)



def timerclick(value):
    global timecount
    timecount += 1

timer = Timer(period=100, mode=Timer.PERIODIC, callback=timerclick)
# funktioniert im Emulator nicht. Mal auf echtem Pico testen
#_thread.start_new_thread(blink, ())
_thread.start_new_thread(asyncout, ())

def timer2str(timer):
    neg = 0
    t = timer
    if t < 0:
        t = abs(t)
        neg = 1
    h = t % 10
    t = int(t / 10)
    s = t % 60
    t = int(t / 60)
    m = t   
    ss = str(s)
    if s < 10:
        ss = "0" + ss
    sm = str(m)
    if m < 10:
        sm = "0" + sm
    if neg == 1:
        sm = "-" + sm[1]
    return sm + ":" + ss + ":" + str(h)

# Funktion zur Taster-Auswertung
while True:
    # print (moderun, mode2sub, mode2run)
    print (timecount)
    if moderun == 0:
        outon = 0 # mode 0 kümmert sich selbst um den LCD
        lcd.move_to(0, 0)
        if modenext == 1:
            lcd.putstr("Stopuhr")
        if modenext == 2:
            lcd.putstr("Count down")
        if modenext == 3:
            lcd.putstr("I love you")
    if moderun == 1:
        outon = 0 
        outs1 = timer2str(timecount-t1) + "  " +timer2str(timecount-t2)
        #lcd.move_to(0, 0)
        #lcd.putstr(outs1)
        outs2 = timer2str(t4) + "  " + timer2str(timecount-t3)
        #lcd.move_to(0, 1)
        #lcd.putstr(outs2)
        outon = 1 
        #asyncout()
    if moderun == 2:
        outon = 0 # mode 2 kümmert sich selbst um den LCD
        if mode2sub == 0:
            lcd.move_to(0, 0)
            lcd.putstr("Anzahl timer")
            lcd.move_to(0, 1)
            lcd.putstr(str(anzcd))
        else:
            lcd.move_to(0, 0)
            lcd.putstr("Timer " + str(cdtimer+1) + ": " + timer2str(acdtimers[cdtimer]))
            lcd.move_to(9+inppos[cdpos], 1)
            lcd.putstr("^")
    if moderun == 3:
        outon = 0 # mode 3 kümmert sich selbst um den LCD
        if mode2sub == 0:
            lcd.move_to(0, 0)
            lcd.putstr("Immer zweimal   ")
            lcd.move_to(0, 1)
            lcd.putstr("mehr wie du!    ")
        if mode2sub == 1:
            lcd.move_to(0, 0)
            lcd.putstr("Ganz, ganz arg  ")
            lcd.move_to(0, 1)
            lcd.putstr("sogar.          ")
        if mode2sub == 2:
            lcd.move_to(0, 0)
            lcd.putstr("Bis zum Mond,und")
            lcd.move_to(0, 1)
            lcd.putstr("wieder zurueck. ")
    if moderun == 4:
        t = acdtimers[cdtimer] + cdstart - timecount
        outon = 0
        outs1 = "Timer " + str(cdtimer+1) + ": " + timer2str(t)
        #lcd.move_to(0, 0)
        #lcd.putstr(outs1)
        outs2 = timer2str(timecount-cdges) + "  " + timer2str(acdtimers[cdtimer+1])
        #lcd.move_to(0, 1)
        #lcd.putstr(outs2)
        outon = 1
        #asyncout()
    #lcd.putstr(str(btn1.value()) + " " + str(btn2.value()) + " " + str(btn3.value()) + " " + str(btn4.value()))
    # mindestens 2 hunderstel müssen zwischen den Tastendrücken liegen zum entprellen.
    if timecount - timebtn > 2:
        if btn2.value() == 0:
            timebtn = timecount
            lcd.clear()
            moderun = 0
            modenext += + 1
            if modenext > 3:
                modenext = 1
        if moderun == 0:
            if btn1.value() == 0:
                timebtn = timecount
                moderun = modenext
                mode2sub = 0
                mode2run = 0
                cdstart = timecount
                t1 = timecount
                t2 = timecount
                t3 = timecount
                t4 = 0
                cdtimer = 0
                cdstart = 0
                cdges = 0
                cdpos = 0
                outon = 0
                outs1 = ""
                outs2 = ""
                lcd.clear()
        elif moderun == 1:
            if btn1.value() == 0:
                timebtn = timecount
                t4 = timecount - t1
                t1 = timecount
                t2 = timecount  
                t3 = timecount
            if btn3.value() == 0:
                timebtn = timecount
                t4 = timecount - t3
                t3 = timecount
            if btn4.value() == 0:
                timebtn = timecount
                t4 = timecount - t2
                t2 = timecount
        elif moderun == 2:
            if mode2sub == 0:
                if btn1.value() == 0:
                    timebtn = timecount
                    mode2sub = 1
                    cdtimer = 0
                    cdpos = 0
                if btn3.value() == 0:
                    timebtn = timecount
                    anzcd -= 1
                if btn4.value() == 0:
                    timebtn = timecount
                    anzcd += 1
            else:
                if btn1.value() == 0:
                    timebtn = timecount
                    lcd.move_to(0, 1)
                    lcd.putstr("                ")
                    cdpos += 1
                    if cdpos == 5:
                        cdpos = 0
                        cdtimer += 1
                        if cdtimer == anzcd:
                            moderun = 4
                            cdtimer = 0
                            mode2run = 0
                if btn3.value() == 0:
                    timebtn = timecount
                    acdtimers[cdtimer] -= incre[cdpos]
                if btn4.value() == 0:
                    timebtn = timecount
                    acdtimers[cdtimer] += incre[cdpos]
        elif moderun == 3:
            if btn3.value() == 0:
                timebtn = timecount
                mode2sub -= 1
            if btn4.value() == 0:
                timebtn = timecount
                mode2sub += 1
        elif moderun == 4:
            if mode2run == 0: #wir warten auf das Starten der CountDown Timer
                cdstart = timecount
                cdges = timecount
                if btn1.value() == 0:
                    timebtn = timecount
                    mode2run = 1
            elif mode2run == 1: #CD-Timer laufen
                if btn1.value() == 0:
                    timebtn = timecount
                    cdtimer += 1
                    if cdtimer > 9:
                        cdtimer = 0
                    cdstart = timecount


