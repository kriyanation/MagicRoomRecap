import subprocess
def expandList(twodlist):
    onedlist = []
    i=0
    for element in twodlist:
        for i in range(0,3):
            onedlist.append(element[i])
            i += 1
    return onedlist
def playtextsound(text,V='m',L='en'):
    '''engine = pyttsx3.init(driverName='espeak')
    engine.setProperty('voice', L+'+'+V+'3')
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()'''
    voiceoutput = subprocess.check_output('espeak-ng -s150 -v'+L+'+f2 \"'+text+'\"',shell=True)
    print("sound"+str(voiceoutput))
