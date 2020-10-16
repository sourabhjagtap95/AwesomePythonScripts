import datetime, time, winsound, sys
from datetime import datetime, timedelta

frequency = 2500  
duration = 2000  

currentTime = time.strftime("%H:%M:%S")

print("")
print ("Currently it is:", currentTime)
minutesOfSleep = int(input("Enter the number of minutes you would like to sleep for:"))
hoursOfSleep = int(input("Enter the number of hours you would like to sleep for:"))
print("")

Alarm = (datetime.now() + timedelta(hours=hoursOfSleep) + timedelta(minutes=minutesOfSleep)).strftime('%H:%M:%S')
print("You will be woken up at:", Alarm)
yesOrNo = str(input("Would you like to set this alarm? [Y/N]")).lower()
print("")

while yesOrNo == "y" or yesOrNo == "yes":

    while currentTime != Alarm:
        print("Currently:", time.strftime("%H:%M:%S"))
        currentTime = time.strftime("%H:%M:%S")
        time.sleep(1)
        if currentTime == Alarm:
            print("Wake up!")       
            for i in range(30):
                winsound.Beep(frequency, duration)
            sys.exit(0)           


            
            
