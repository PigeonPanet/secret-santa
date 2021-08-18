import random
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_ADDRESS = ''
PASSWORD = ''

s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
s.starttls()
s.login(EMAIL_ADDRESS, PASSWORD)

participant = []
randPlayer = []
finish = False

def checkExist(r) :
    try:
         randPlayer.index(r)
         return True
    except ValueError :
        return False           

def fillRandPlayler():
    while len(randPlayer) != len(participant):
        for e in participant:
            numRandom = random.randint(1, len(participant))
            exist = checkExist(numRandom)
            if exist == False :
                randPlayer.append(numRandom)


def attributParticipant():
    for e in participant:
        for i in range(len(randPlayer)):
            e[2] = randPlayer[i]
            randPlayer.pop(i)
            break

def reload(): 
    global participant,randPlayer,finish
    participant = [
        ['Matthieu', 1, 0, 'Matthieu@yopmail.com'],
        ['Marc', 2, 0, 'Marc@yopmail.com'],
        ['Margot', 3, 0, 'Luc@yopmail.com'],
        ['Jean', 4, 0, 'Jean@yopmail.com'],
    ]

    randPlayer = []
    finish = False    


def checkFinish():
    for e in participant:
        if e[1] == e[2] or e[2] == 0 :
            return False
    return True


def startRandom():
    global participant,randPlayer,finish
    reload()
    while finish == False: 
        reload()              
        fillRandPlayler()
        attributParticipant()
        finish = checkFinish()
    saveLocalResponse()
    sendEmail()


def saveLocalResponse():
    file = open('secretSanta.txt','w') 
    for e in participant:
        for e2 in participant:
            if e[2] == e2[1]:
                file.write(e[0] + ' ===> ' + e2[0] +'\n') 
                print(e[0] + ' ===> ' + e2[0])
    
    file.close() 


def sendEmail():
    try:
        global participant,randPlayer,finish
        for e in participant:
            for e2 in participant:
                if e[2] == e2[1]:
                    print(e[0] + ' ===> ' + e2[0])
                    msg = MIMEMultipart() 

                    # add in the actual person name to the message template
                    message = 'Tu dois offrir un cadeau à ' + e2[0] + '. \n'

                    # setup the parameters of the message
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = e[3]
                    msg['Subject'] = "SECRET SANTA" + str(datetime.datetime.now().year) + " !!!"

                    # add in the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # send the message via the server set up earlier.
                    s.send_message(msg)
                    
                    del msg
    except:
        print('error email')

startRandom()
