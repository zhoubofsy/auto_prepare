#!/usr/bin/python
#coding:utf-8

import subprocess as proc
import argparse
import pdb

def cmd_exec2(cmd,cmd_type=True):
    ret = -1
    if cmd == "":
        return ret

    command = []
    command.append(cmd)
    p = proc.Popen(command,stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT, shell=cmd_type)
    ret = p.wait()
    if 0 != ret:
        for line in p.stdout.readline():
            print line
    return ret

def cmd_exec(cmd, cmd_type=True):
    #pdb.set_trace()
    ret = -1
    if cmd == "":
        return ret

    command = cmd.split(' ')
    p = proc.Popen(command,stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT, shell=cmd_type)
    ret = p.wait()
    if 0 != ret:
        for line in p.stdout.readline():
            print line
    return ret

def service_start(ser_name):
    ret = -1
    if ser_name == "":
        return ret
    
    # service ser_name start
    cmd = "service " + ser_name + " start"
    ret = cmd_exec(cmd,False)
    return ret

def service_stop(ser_name):
    ret = -1
    if ser_name == "":
        return ret

    # service ser_name stop
    cmd = "service " + ser_name + " stop"
    ret = cmd_exec(cmd,False)
    return 0

def service_add(ser_name):
    ret = -1
    if ser_name == "":
        return ret
    # service add
    # service on
    ret = do_add(ser_name)
    if ret == 0:
        ret = service_on(ser_name)
        if ret != 0:
            do_del(ser_name)
    return ret

def service_del(ser_name):
    ret = -1
    if ser_name == "":
        return ret
    # service off
    # service delete
    ret = service_off(ser_name)
    if ret == 0:
        ret = do_del(ser_name)
        if ret != 0:
            service_on(ser_name)
    return ret

def service_on(ser_name):
    ret = -1
    if ser_name == "":
        return ret

    # chkconfig ser_name on
    cmd = "chkconfig " + ser_name + " on"
    ret = cmd_exec(cmd,False)
    return ret

def service_off(ser_name):
    ret = -1
    if ser_name == "":
        return ret

    # chkconfig ser_name off
    cmd = "chkconfig " + ser_name + " off"
    ret = cmd_exec(cmd,False)
    return ret

def do_add(ser_name):
    ret = -1
    if ser_name == "":
        return ret

    # chkconfig --add ser_name
    cmd = "chkconfig " + "--add " + ser_name
    ret = cmd_exec(cmd,False)
    return ret

def do_del(ser_name):
    ret = -1
    if ser_name == "":
        return ret
    
    # chkconfig --del ser_name
    cmd = "chkconfig " + "--del " + ser_name
    ret = cmd_exec(cmd,False)
    return ret

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="start or stop service; add or del service", nargs=1)
    parser.add_argument("-s", "--service", help="service name", nargs=1)
    args = parser.parse_args()

    action = args.action[0]
    service = args.service[0]

    if action == 'start':
        # start service
        service_start(service)
    elif action == 'stop':
        # stop service
        service_stop(service)
    elif action == 'add':
        # add service
        service_add(service)
    elif action == 'del':
        # delete service
        service_del(service)
    else:
        print "Unknow Action"
