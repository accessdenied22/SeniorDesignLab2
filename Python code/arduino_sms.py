import serial
import time
from datetime import datetime
import smtplib
import atexit

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM11', 9800, timeout=1)
time.sleep(2)

def exit_handler():
    print("Program exiting")
    ser.close()

atexit.register(exit_handler)


CARRIERS = {
	'att':     'txt.att.net',
	'tmobile': 'tmomail.net',
	'verizon': 'vtext.com',
	'boost':   'sms.myboostmobile.com',
	'cricket': 'sms.cricketwireless.net',
	'usc':     'email.uscc.net'
}
#PHONE = '3192106233'
#PROVIDER = 'tmobile'

PHONE = '3195199295'
PROVIDER = 'att'

def sendSMS():
    timestamp = datetime.now().strftime("%I:%M %p on %m/%d/%Y")   
    text = "Critical Safety Event at "+timestamp # HH:MM XX on Month/Day/2022
    to_number = f"{PHONE}@{CARRIERS[PROVIDER]}"
    auth = ('teamaccessdenied22@gmail.com', 'vvgpsxsftdcxovmb')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    message = 'Subject: {}\n\n{}'.format("", text)
    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)

last_received = []
buffer_string = ''
THRESH = 150
while True:
    buffer_string = buffer_string + ser.read(ser.inWaiting()).decode()
    if ',' in buffer_string:
        lines = buffer_string.split(',') # Guaranteed to have at least 2 entries
        
        if(len(lines) > 1):
            buffer_string = lines[-1]
            last_val = lines[-2]
            if(last_val != ''):
                num = int(last_val) # convert the unicode string to an int
                
                last_received.append(num)
                if(len(last_received) > 5): 
                    last_received = last_received[1:]            
                    if(num < THRESH and last_received[-2] < THRESH and last_received[-4] >= THRESH and last_received[-3] >= THRESH):
                        print(f"Beam obstruction: {num}")
                        sendSMS()
            
ser.close()