import time
#from gpiozero import button
zeiten = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
anz = input("Anzahl der Zeiten?")
anz=int(anz)
print (anz)
i = 0
while i < anz:
    zeiten[i] = input("Zeit")
    zeiten[i] = int(zeiten[i])
    i += 1
i = 0    
while i < anz:
    print (zeiten[i])
    start = time.time()
    dauer = 0
    while dauer < zeiten[i]:
        ende = time.time()
        dauer = ende - start
        print (zeiten[i]-dauer)
    i += 1
    