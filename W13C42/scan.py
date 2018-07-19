# -*- coding:utf-8 -*-

import socket
import getopt
import sys
import re

def scan(host,port):
    rdict = {}
    result = ''
    port = list(port)
    for p in port:
        s = socket.socket()
        try:
            s.connect((host,p))
            s.close()
            rdict[p] = 'open'
        except ConnectionRefusedError:
            rdict[p] = 'closed'
    for key, val in rdict.items():
        result += '{} {}'.format(key,val)
        result += '\n'

    return result

if __name__ == '__main__':
    
    opts, args = getopt.getopt(sys.argv[1:],"",["host=","port="])
    port = []
    host = ''
    for opt,val in opts:
        if str(opt) == '--host':
            if re.match(r'\d+\.\d+\.\d+\.\d+',str(val)):
                host = str(val)
            else:
                print('Parameter Error')
                exit()
        elif str(opt) == '--port':
            if re.match(r'\d+\-\d+',str(val)):
                num1,num2 = str(val).split('-')
                num1,num2 = int(num1),int(num2)
                if num1 > num2:
                    for i in range(num2,(num1 + 1)):
                        port.append(int(i))
                elif num1 == num2:
                    print('Parameter Error')
                    exit()
                else:
                    for i in range(num1,(num2 + 1)):
                        port.append(int(i))
            elif re.match(r'\d+',str(val)):
                port.append(int(val))
            else:
                print('Parameter Error')
                exit()
        else:
            print('Parameter Error')
            exit()

    print(scan(host,port))

