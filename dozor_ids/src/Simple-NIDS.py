from scapy.all import *
from sys import argv
import logging
import datetime
import os
import RuleFileReader
from Sniffer import *

RED = '\033[91m'
BLUE = '\033[34m'
GREEN = '\033[32m'
ENDC = '\033[0m'



def main(filename, iface):
    """Read the rule file and start listening."""

    now = datetime.now()
    date = now.date()
    name = 'log_' + str(date) + '.json'
    if not os.path.exists('./logs/' + name):
        with open('./logs/' + name, 'w', encoding='utf-8') as file:
            pass
            
    
    logging.basicConfig(filename= "Simple-NIDS " + str(now) + '.log',level=logging.INFO)

    print("Simple-NIDS started.")
    # Read the rule file
    print("Reading rule file...")
    global ruleList
    ruleList, errorCount = RuleFileReader.read(filename)
    print("Finished reading rule file.")

    if (errorCount == 0):
        print("All (" + str(len(ruleList)) + ") rules have been correctly read.")
    else:
        print(str(len(ruleList)) + " rules have been correctly read.")
        print(str(errorCount) + " rules have errors and could not be read.")

    sniffer = Sniffer(ruleList, log_file=name, iface=iface)
    sniffer.start()


ruleList = list()
script, filename, iface = argv
main(filename, iface)
