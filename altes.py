
# Text in Zeilen
zeile_oben  = 'Hello World';
zeile_unten = 'Hurra ich lebe'

# Display-Zeilen ausgeben
lcd.putstr(zeile_oben + "\n" + zeile_unten)
sleep_ms(3000)

# Display-Inhalt löschen
lcd.clear()
sleep_ms(1000)

# Position im Display
for zeile in range (0,2):
    for spalte in range (0,16):
        lcd.move_to(spalte, zeile)
        lcd.putstr('.')
        sleep_ms(300)

print("Hintergrundlicht aus")
lcd.backlight_off()
sleep_ms(3000)

print("Hintergrundlicht an")
lcd.backlight_on()
sleep_ms(3000)

print("Display aus")
lcd.display_off()
sleep_ms(3000)

print("Display an")
lcd.display_on()
sleep_ms(3000)


def on_pressed_b1(timer):
    global t1, t2, t3, t4, timecount
    t4 = timecount - t1
    t1 = timecount
    t2 = timecount
    t3 = timecount

def on_pressed_b2(timer):
    global t1, t2, t3, t4, timecount
    x=1

def on_pressed_b3(timer):
    global t1, t2, t3, t4, timecount
    t4 = timecount - t2
    t2 = timecount

def on_pressed_b4(timer):
    global t1, t2, t3, t4, timecount
    t4 = timecount - t3
    t3 = timecount

def btn_debounce_b1(pin):
    Timer().init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed_b1)

def btn_debounce_b2(pin):
    Timer().init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed_b2)

def btn_debounce_b3(pin):
    Timer().init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed_b3)

def btn_debounce_b4(pin):
    Timer().init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed_b4)

btn1.irq(handler=btn_debounce_b1, trigger=Pin.IRQ_RISING)    
btn2.irq(handler=btn_debounce_b2, trigger=Pin.IRQ_RISING)    
btn3.irq(handler=btn_debounce_b3, trigger=Pin.IRQ_RISING)    
btn4.irq(handler=btn_debounce_b4, trigger=Pin.IRQ_RISING)    

