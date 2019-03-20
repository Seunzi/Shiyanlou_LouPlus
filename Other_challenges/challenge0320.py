# -*- coding: utf-8 -*-
# Challenge topic: https://www.shiyanlou.com/challenges/2682

import sys, os, getopt, json

#SERVER_INFO_PATH = '/home/shiyanlou/serverinfo'
SERVER_INFO_PATH = 'serverinfo'

# dict example:
# {
#   '127.0.0.1':{'user':'shiyanlou','passwd':'shiyanlou'},
#   '127.0.0.2':{'user':'shiyanlou02','passwd':'shiyanlou02'}
# }

servers_dict = {}
if os.path.isfile(SERVER_INFO_PATH) and os.stat(SERVER_INFO_PATH).st_size > 0:
    with open(SERVER_INFO_PATH,'r') as file:
        servers_dict = json.load(file)

hostIp_list = []
if servers_dict:
    for hostIp in servers_dict:
        hostIp_list.append(hostIp)

def add_server(hostIp,user,passwd):
    if hostIp not in hostIp_list:
        servers_dict[str(hostIp)] = {'user':str(user),'passwd':str(passwd)}
        with open(SERVER_INFO_PATH,'w') as file:
            json.dump(servers_dict,file)
    else:
        print('ERROR: {} are already existed.'.format(hostIp))

def list_server():
    for hostIp, detail in servers_dict.items():
        print('{} {} {}'.format(hostIp,detail['user'],detail['passwd']))

def delete_server(hostIp):
    servers_dict.pop(str(hostIp),None)
    with open(SERVER_INFO_PATH,'w') as file:
        json.dump(servers_dict,file)

def get_arg(optlist,iopt):
    for opt,arg in optlist:
        if str(opt) == str(iopt):
            return arg
    return None

def run():
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        print('No command found.')
        return None
    
    optList, argList = getopt.getopt(sys.argv[2:],"h:u:p:")
    
    if action == 'add':
        hostIp = get_arg(optList,'-h')
        user = get_arg(optList,'-u')
        passwd = get_arg(optList,'-p')
        if hostIp and user and passwd:
            add_server(hostIp,user,passwd)
        else:
            print('ERROR: Parameter error during add command.')
    
    elif action == 'list':
        list_server()
    
    elif action == 'delete':
        hostIp = get_arg(optList,'-h')
        if hostIp:
            delete_server(hostIp)
        else:
            print('ERROR: Parameter error during delete command.')
    
    else:
        print('ERROR: Command unracognized or unknow.')

if __name__ == '__main__':
    run()
