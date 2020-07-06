
import subprocess
import pyttsx3, sys

_isLinux = sys.platform.startswith('linux')
if not _isLinux:
    import pythoncom
def expandList(twodlist):
    onedlist = []
    i=0
    for element in twodlist:
        for i in range(0,3):
            onedlist.append(element[i])
            i += 1
    return onedlist

def expandImageList(twodlist):
    onedlist = []
    i=0
    for element in twodlist:
        for i in range(0,3):
            onedlist.append((element[0],element[i+1]))
            i += 1
    return onedlist

def playtextsound(text,V='m',L='en'):
    if _isLinux:
        engine = pyttsx3.init(driverName='espeak')
    else:
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
    engine.setProperty('voice', 'en+f2')
    engine.setProperty('rate', 130)
    engine.setProperty("volume", 0.9)
    engine.say(text)
    #  engine.say(text)
    engine.runAndWait()
    #voiceoutput = subprocess.check_output('espeak-ng -s150 -v'+L+'+f2 \"'+text+'\"',shell=True)
    #print("sound"+str(voiceoutput))
