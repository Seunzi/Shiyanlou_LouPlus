#!/usr/bin/env/python3

import sys

def caltax(sal,itax,rate,dedu):
    tax = itax * rate - dedu
    osal = sal * (1-0.165) - tax
    return(format(osal,".2f"))

def calselect(sal):
    itax = sal * (1 - 0.165) - 3500
    if itax < 0:
        itax = 0
    
    if sal < 3500:
        return(sal)
    elif itax <= 1500:
        return(caltax(sal,itax,0.03,0))
    elif itax <= 4500:
        return(caltax(sal,itax,0.1,105))
    elif itax <= 9000:
        return(caltax(sal,itax,0.2,555))
    elif itax <= 35000:
        return(caltax(sal,itax,0.25,1005))
    elif itax <= 55000:
        return(caltax(sal,itax,0.30,2755))
    elif itax <= 80000:
        return(caltax(sal,itax,0.35,5505))
    else:
        return(caltax(sal,itax,0.45,13505))
 
try:
    idlist = []
    taxlist = []
   
    for arg in sys.argv[1:]:
        idsal = arg.split(':')
        iid = int(idsal[0])
        idlist.append(iid)
        sal = int(idsal[1])
        taxlist.append(calselect(sal))
    
    n = 0   
    while n < len(idlist):
        print("{}:{} ".format(idlist[n],taxlist[n]))
        n += 1
except ValueError:
    print("Parameter Error")

