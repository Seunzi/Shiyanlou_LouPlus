#!/usr/bin/env python3

import sys


def caltax(salary,rate,deduct):
    tex = format(salary * rate - deduct,".2f")
    print(tex)

if __name__ == '__main__':
    try:
        salary = int(sys.argv[1]) - 3500
        if salary < 1500:
            caltax(salary,0.03,0)
        elif salary < 4500:
            caltax(salary,0.10,105)
        elif salary < 9000:
            caltax(salary,0.20,555)
        elif salary < 35000:
            caltax(salary,0.25,1005)
        elif salary < 55000:
            caltax(salary,0.30,2755)
        elif salary < 80000:
            caltax(salary,0.35,5505)
        elif salary > 80000:
            caltax(salary,0.45,13505)
    except ValueError:
        print("Parameter Error")

 
