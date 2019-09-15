"""
This is timer.py, it uses sys.argv to do a timer, which creates a noise when complete

Exit Codes
0: Success
1: Wrong Number of Args
2: Invalid Args
"""
# Code
try:
    from playsound import playsound # Import Playsound
except:
    print("Please use pip to install 'playsound' by using 'pip install playsound'")
    quit()

from sys import argv, stdout # Import Argv
import time
from os import chdir

# class for print on line
class PrintOnLine():
    def __init__(self):
        self.last_print_len = 0
    def __call__(self, string):
        print(string+" "*(self.last_print_len-len(string)), end="\r")
        self.last_print_len = len(string)
    def clear(self):
        print(""*self.last_print_len, end="\r")
        self.last_print_len = 0
    def __del__(self):
        self.clear()
        chdir("bin")

print_on_line = PrintOnLine()

SETTINGS_LENGTH = 1

# Time Units
# KWICK MAFS
MINUTE = 60
HOUR   = MINUTE*60
DAY    = HOUR*24
WEEK   = DAY*7
MONTH  = DAY*30
YEAR   = DAY*256
DECADE = YEAR*10


TIME_UNITS = {
    "seconds"     :1     ,
    "decaseconds" :10** 1,
    "hectoseconds":10** 2,
    "kiloseconds" :10** 3,
    "megaseconds" :10** 6,
    
    "minutes":MINUTE,
    "hours"  :HOUR,
    "days"   :DAY,
    "weeks"  :WEEK,
    "months" :MONTH,
    "years"  :YEAR,
    "decades":DECADE,

    #  Stuff from https://en.wikipedia.org/wiki/Unit_of_time#List
    "moments"   :90,
    "quarters"  :MINUTE*15,
    "kes"       :(60*15)-36,
    "fortnights":DAY*14,
    "semesters" :MONTH*6,
    "seasons"   :MONTH*3,
    "jubilees"  :DECADE*5,
}

if len(argv) < 2:
    print("Please put at least two args")
    exit(1)

if argv[1] == "settings":
    if len(argv) < 4:
        print("Please put at least four args for settings")
        quit()
    with open("settings.txt", "r") as file:
        lines = file.readlines()
    
    for i in range(SETTINGS_LENGTH-len(lines)):
        lines.append("")

    if argv[2] == "change-song":
        # Using stdout to avoid flushing
        stdout.write(f"Song Changed From '{lines[0]}' ")
        lines[0] = argv[3]
        stdout.write(f"to '{lines[0]}'.")
        stdout.flush()

    else:
        print(f"{argv[2]} is not a valid settings.")
    with open("settings.txt", "w") as file:
        file.writelines(lines)
else:
    try:
        time_num = int(argv[1])
    except:
        print("Please Type A Valid Command/Int")
        exit(2)
    
    try:
        time_num *= TIME_UNITS[argv[2]]
    except:
        try:
            time_num *= TIME_UNITS[argv[2]+"s"]
        except:
            print("Please Type A Valid Unit")

    time_left = time_num
    while time_left > 0:
        print_on_line(f"{time_left//60} minutes and {time_left%60} seconds left..." if time_left > 59 else f"{time_left} seconds left...")
        time.sleep(1)
        time_left -= 1
    
    with open("settings.txt", "r") as file:
        print_on_line("Control-C to end ringtone")
        song = file.readlines()[0]
        while True:
            try:
                playsound(f"songs/{song}.mp3")
            except KeyboardInterrupt:
                print_on_line((" "*26)+" < Type Y or N, it quits either way.") # 26 is the length of dO yOu WaNt To KiLl (Y/n)
                exit(0)
            except IndexError:
                print_on_line((" "*26)+" Wierd Bug?")
                exit(0)
