from threading import Thread
from scapy.all import *
import logging
import datetime
import RuleFileReader
from Rule import *
import json

def CreateFileLogs():
    now = datetime.now()
    date = now.date()
    name = 'log_' + str(date) + '.json'
    with open('./logs/log_' + str(date) + '.json', 'w+', encoding='utf-8') as file:
        pass
    return name

class Sniffer(Thread):
    def __init__(self, ruleList, iface, log_file = './logs/test.json'):
        Thread.__init__(self)
        self.stopped = False
        self.ruleList = ruleList
        self.log_file = log_file
        self.iface = iface

    def stop(self):
        self.stopped = True

    def stopfilter(self, x):
        return self.stopped

    def inPacket(self, pkt):

        for rule in self.ruleList:
            # Check all rules
            # print("checking rule")
            print(pkt)
            matched = rule.match(pkt)
            if (matched):
                logMessage = rule.getMatchedMessage(pkt)
                logging.warning(logMessage)

                print(rule.getMatchedPrintMessage(pkt))

            '''FOR JSON'''
            if (matched):
                logMessage = json.dumps(rule.getMatchedMessageJSON(pkt)) + '\n'
                now = datetime.now()
                curr_date = str(now.date())
                tmp_ = self.log_file.split('_')
                tmp = tmp_[1].split('.')

                if (curr_date != tmp[0]):
                    print('!!!!!!!!!!!!!!!!!!!!!')
                    self.log_file = CreateFileLogs()
                
                with open('./logs/' + self.log_file, 'a', encoding='utf-8') as file:
                    file.write(logMessage)

                



    def run(self):
        print("Sniffing started.")
        sniff(prn=self.inPacket, filter="", store=0, stop_filter=self.stopfilter, iface=self.iface)
