# -*- coding:utf-8 -*-

import re
from datetime import datetime
from pandas import DataFrame

def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   '(\d+.\d+.\d+.\d+)\s-\s-\s'
                   '\[(.+)\]\s'
                   '"GET\s(.+)\s\w+/.+"\s'
                   '(\d+)\s'
                   '(\d+)\s'
                   '"(.+)"\s'
                   '"(.+)"'
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    ip_dict = {}
    url_dict = {}

    cols = ['IP','Time','Url','Status','Size','Head','Client']
    df_log = DataFrame(logs,columns=cols)
    max_ip_addr = df_log[df_log['Time'].str.contains('11/Jan/2017')].groupby('IP').size().argmax()
    max_ip_num = df_log[df_log['Time'].str.contains('11/Jan/2017')].groupby('IP').size().max()
    ip_dict[max_ip_addr] = int(max_ip_num)

    max_404_url = df_log[df_log['Status'].str.contains('404')].groupby('Url').size().argmax()
    max_404_num = df_log[df_log['Status'].str.contains('404')].groupby('Url').size().max()
    url_dict[max_404_url] = int(max_404_num)

    
    return ip_dict, url_dict

if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
