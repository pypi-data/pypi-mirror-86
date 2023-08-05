import tzlocal
from datetime import datetime

def human_time(logtime):
    """
    Converts seconds since epoch to a human-readable time format.

    Code taken from: jfs's answer on
    https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date/40769643#40769643

    Input:
        logtime: time in seconds, since epoch.

    Output:
        str: a human readable format of the time.
    """

    local_timezone = tzlocal.get_localzone() # get pytz timezone
    local_time = datetime.fromtimestamp(logtime, local_timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

with open("records.log", "r") as file:
    lines = file.readlines()
    last = 0
    begin = True
    for i in range(0, len(lines)):
        time = lines[i]
        time = time.split(",")[0]
        if time[-4:]=="line":
            time=time[:-4]
        time=float(time)
        #print(time)
        if time - last > 31:
            print(str(i)+","+human_time(time)+","+human_time(last)+","+str(time-last))
            begin = False
        last=time
        assert(last==time)

print("--")
with open("out2.log", "r") as file:
    lines = file.readlines()
    last = 0
    begin = True
    for i in range(0, len(lines)):
        if lines[i][0:14] == "DEBUG:root:160":
            time = lines[i][11:]
            time = time.split(" ")[0]
            if time[-4:]=="line":
                time=time[:-4]
            time=float(time)
            #print(time)
            if time - last > 31:
                print(str(i)+","+human_time(time)+","+human_time(last)+","+str(time-last))
                begin = False
            last=time
            assert(last==time)
    print("Last recorded time: " + human_time(time))
