from ipaddress import *
from scapy.all import *
from Utils import *
from Action import *
from Protocol import *
from IPNetwork import *
from Ports import *
from PacketStrings import *

class Rule:
    def __init__(self, str):
        self.string = str

        str = str.strip()
        strs = str.split(' ')

        if (len(strs) >= 7):

            self.action = action(strs[0])
            self.protocol = protocol(strs[1])
            try:
                self.srcIps = IPNetwork(strs[2])
            except:
                raise ValueError("Invalid rule : incorrect source ips : '" + strs[2] + "'.")
            try:
                self.srcPorts = Ports(strs[3])
            except:
                raise ValueError("Invalid rule : incorrect source ports : '" + strs[3] + "'.")
            try:
                self.dstIps = IPNetwork(strs[5])
            except:
                raise ValueError("Invalid rule : incorrect destination ips : '" + strs[5] + "'.")

            try:
                self.dstPorts = Ports(strs[6])
            except:
                raise ValueError("Invalid rule : incorrect destination ports : '" + strs[6] + "'.")
            strs = str.split('(')
            if (len(strs) >= 2):
                if (strs[-1][-1] == ')'):
                    strs[-1] = strs[-1][:-1]
                opts = strs[1].split(';')
                for opt in opts:
                    kv = opt.split(':',1)
                    if (len(kv) >= 2):
                        option = kv[0].strip()
                        value = kv[1].strip()

                        if (option == "msg"):
                            self.msg = value
                        elif (option == "tos"):
                            self.tos = int(value)
                        elif (option == "len"):
                            self.len = int(value)
                        elif (option == "offset"):
                            self.offset = int(value)
                        elif (option == "seq"):
                            self.seq = int(value)
                        elif (option == "ack"):
                            self.ack = int(value)
                        elif (option == "flags"):
                            self.flags = value
                        elif (option == "http_request"):
                            self.http_request = value
                            if (self.http_request.endswith('"')):
                                self.http_request = self.http_request[:-1]
                            if (self.http_request.startswith('"')):
                                self.http_request = self.http_request[1:]
                        elif (option == "content"):
                            self.content = value
                            if (self.content.endswith('"')):
                                self.content = self.content[:-1]
                            if (self.content.startswith('"')):
                                self.content = self.content[1:]
                        else:
                            raise ValueError("Invalid rule : incorrect option : '" + option + "'.")
        else:
            raise ValueError("Invalid rule : a rule must include mandatory elements : action protocol src_ips src_ports -> dst_ips dst_ports")

    def __repr__(self):
        return self.string

    def match(self, pkt):
        if (not self.checkProtocol(pkt)):
            return False

        if (not self.checkIps(pkt)):
            return False

        if (not self.checkPorts(pkt)):
            return False

        if (not self.checkOptions(pkt)):
            return False

        return True

    def checkProtocol(self, pkt):
        f = False
        if (self.protocol == Protocol.TCP and TCP in pkt):
            f = True
        elif (self.protocol == Protocol.UDP and UDP in pkt):
            f = True
        elif (self.protocol == Protocol.HTTP and TCP in pkt):
            if (isHTTP(pkt)):
                f = True
        return f

    def checkIps(self, pkt):
        f = False
        if (IP not in pkt):
            f = False
        else:
            srcIp = pkt[IP].src
            dstIp = pkt[IP].dst
            ipSrc = ip_address(srcIp)
            ipDst = ip_address(dstIp)
            if (self.srcIps.contains(ipSrc) and self.dstIps.contains(ipDst)):
                f = True
            else:
                f = False
        return f

    def checkPorts(self, pkt):
        f = False
        if (UDP in pkt):
            srcPort = pkt[UDP].sport
            dstPort = pkt[UDP].dport
            if (self.srcPorts.contains(srcPort) and self.dstPorts.contains(dstPort)):
                f = True
        elif (TCP in pkt):
            srcPort = pkt[TCP].sport
            dstPort = pkt[TCP].dport
            if (self.srcPorts.contains(srcPort) and self.dstPorts.contains(dstPort)):
                f = True
        return f

    def checkOptions(self, pkt):
        if (hasattr(self, "tos")):
            if (IP in pkt):
                if (self.tos != int(pkt[IP].tos)):
                    return False
            else:
                return False

        if (hasattr(self, "len")):
            if (IP in pkt):
                if (self.len != int(pkt[IP].ihl)):
                    return False
            else:
                return False

        if (hasattr(self, "offset")):
            if (IP in pkt):
                if (self.offset != int(pkt[IP].frag)):
                    return False
            else:
                return False

        if (hasattr(self, "seq")):
            if (TCP not in pkt):
                return False
            else:
                if (self.seq != int(pkt[TCP].seq)):
                    return False

        if (hasattr(self, "ack")):
            if (TCP not in pkt):
                return False
            else:
                if (self.ack != int(pkt[TCP].ack)):
                    return False

        if (hasattr(self, "flags")):
            if (TCP not in pkt):
                return False
            else:
                for c in self.flags:
                    pktFlags = pkt[TCP].underlayer.sprintf("%TCP.flags%")
                    if (c not in pktFlags):
                        return False

        if (hasattr(self, "http_request")):
            if (not isHTTP(pkt)):
                return False
            elif (TCP in pkt and pkt[TCP].payload):
                data = str(pkt[TCP].payload)
                words = data.split(' ')
                if ((len(words) < 1) or (words[0].rstrip() !=  self.http_request)):
                    return False
            else:
                return False

        if (hasattr(self, "content")):
            payload = None
            if (TCP in pkt):
                payload = pkt[TCP].payload
            elif (UDP in pkt):
                payload = pkt[UDP].payload
            if (payload):
                if (self.content not in str(payload)):
                    return False
            else:
                return False

        return True

    def getMatchedMessage(self, pkt):
        msg = ""
        if (self.action == Action.ALERT):
            msg += " ALERT "
        if hasattr(self, "msg"):
            msg += self.msg  + "\n"

        msg += "Rule matched :\n" + str(self) + "\n"
        msg += "By packet :\n" + packetString(pkt) + "\n"

        return msg

    def getMatchedPrintMessage(self, pkt):
        msg = ""
        if (self.action == Action.ALERT):
            msg += RED + "ALERT "
        if hasattr(self, "msg"):
            msg += self.msg
        msg += "\n" + ENDC

        msg += "Rule matched :\n" + str(self) + "\n"
        msg += "By packet :\n" + matchedPacketString(pkt, self) + "\n"

        return msg
    

    ''' JSON format '''

    def getMatchedMessageJSON(self, pkt):
        msg = {}
        msg['time'] = str(datetime.now())
        if (self.action == Action.ALERT):
            msg['action'] = "ALERT"
        if hasattr(self, "msg"):
            msg['msg'] = self.msg
        msg['pkt'] = packetStringJSON(pkt)
        return msg