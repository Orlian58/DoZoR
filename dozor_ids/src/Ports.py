class Ports:
    def __init__(self, string):
        try:
            if (string == "any"):
                self.type = "any"
            elif(":" in string):
                self.type = "range"
                strs = string.split(":")
                if (string[0] == ":"):
                    self.lowPort = -1
                    self.highPort = int(strs[1])
                elif(string[len(string) - 1] == ":"):
                    self.lowPort = int(strs[0])
                    self.highPort = -1
                else:
                    self.lowPort = int(strs[0])
                    self.highPort = int(strs[1])
            elif("," in string):
                self.type = "list"
                self.listPorts = list()
                strs = string.split(",")
                for s in strs:
                    self.listPorts.append(int(s))
            else:
                self.type = "list"
                self.listPorts = list()
                self.listPorts.append(int(string))
        except:
            raise ValueError("Incorrect input string.")

    def contains(self, port):
        if (self.type == "any"):
            return True
        elif (self.type == "range"):
            if (self.lowPort == -1):
                return port <= self.highPort
            elif (self.highPort == -1):
                return port >= self.lowPort
            else:
                return self.lowPort <= port and port <= self.highPort
        elif (self.type == "list"):
            return port in self.listPorts

    def __repr__(self):
        if (self.type == "any"):
            return "any"
        elif (self.type == "range"):
            if (self.lowPort == -1):
                return ":" + str(self.highPort)
            else:
                if (self.highPort == -1):
                    return str(self.lowPort) + ":"
                else:
                    return str(self.lowPort) + ":" + str(self.highPort)
        elif (self.type == "list"):
            return self.listPorts.__repr__()
