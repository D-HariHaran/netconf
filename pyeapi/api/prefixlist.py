#
# Module to list and edit prefix list.
#
import pyeapi
import re

from pyeapi.api import EntityCollection

prefix_re = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}"
#r = re.compile(r'^ip\sprefix-list\s([a-zA-Z0-9].*)\sseq\s(\d+)\s((?:permit|deny))\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})$', re.M)
#r1 = re.compile(r'^ip\sprefix-list\s([a-zA-Z0-9].*)\sseq\s\d+\s(?:permit|deny)\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', re.M)

class PrefixLists(EntityCollection):
    """
    Class which contains prefix list functions.
    """
    def getall(self):
        return self.get(self.getallName())

    def get(self, prefixlist):
        temp1 = []
        for prefix in prefixlist:
            temp2 = {}
            temp2["name"] = prefix
            #print(prefix)
            r = re.compile(r'^ip\sprefix-list\s'+prefix+'[\s\n].*[seq\s(\d+)\s((?:permit|deny))\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})]*$',re.M)
            if not (r.findall(self.config).__len__() > 0):
                print("if")
                rr = re.compile(r'^ip\sprefix-list\s' + prefix + '[seq\s(\d+)\s((?:permit|deny))\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})].*$',re.M)
                l1 = r.findall(self.config) + rr.findall(self.config)
            else:
                print("else")
                l1 = r.findall(self.config)
            print(l1)
            r1 = re.compile(r'seq\s(\d+)\s((?:permit|deny))\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})$', re.M)
            l2 = []
            if l1.__len__() > 0:
                for i in l1:
                    l2 += r1.findall(i)
            temp4 = []
            for i in l2:
                temp3 = {}
                temp3["seq"] = i[0]
                temp3["action"] = i[1]
                temp3["prefix"] = i[2]
                temp4.append(temp3)
                temp2["value"] = temp4
            temp1.append(temp2)
        return temp1

    def getallName(self):
        r1 = re.compile(
            r'^ip\sprefix-list\s([a-zA-Z0-9].*)seq\s\d+\s(?:permit|deny)\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$',
            re.M)
        r2 = re.compile(
            r'^ip\sprefix-list\s([a-zA-Z0-9].*)\n\s.*seq\s\d+\s(?:permit|deny)\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$',
            re.M)
        return set(r1.findall(self.config) + r2.findall(self.config))

    def add(self, name, seqno, action, prefix):
        return self.configure('ip prefix-list %s seq %s %s %s' % (name, seqno, action, prefix))

    def delete(self, name, seqno, action, prefix):
        return self.configure('no ip prefix-list %s seq %s %s %s' % (name, seqno, action, prefix))

def instance(api):
    return PrefixLists(api)

if __name__ == '__main__':
    node = pyeapi.connect(transport="https", username="admin", password="admin", host="192.168.220.170",enablepwd="siva", return_node=True)
    pl = node.api("prefixlist")
    print(pl())