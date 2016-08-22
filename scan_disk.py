#!/usr/bin/python
#coding:utf8

import subprocess as proc
import argparse
import pdb

# scan disk devices
# lsblk -l --output KNAME,TYPE,MOUNTPOINT | awk '$2 == "disk" {print $0}' | awk '$3 == "" {print $0}'
# xvda  disk
# xvdb  disk

# scan disk's part
# fdisk -l /dev/xvda | awk '/^\/dev\//{print $0}'
# /dev/xvda1   *           1          64      512000   83  Linux
# /dev/xvda2              64        2611    20458496   8e  Linux LVM

#auto:
def auto_scan_disk():
    #pdb.set_trace()
    unuse = []
    um_disks = []

    # list unmount disk
    um_disks = scan_unmount_disks()

    # check part
    for disk in um_disks:
        if not is_exsit_part(disk):
            unuse.append(disk)
    return unuse

def scan_unmount_disks():
    unmount_disks = []
    exec_cmd = ["lsblk -l --output KNAME,TYPE,MOUNTPOINT | awk '$2 == \"disk\" { print $0 }' | awk '$3 == \"\" { print $0 }'"]

    p = proc.Popen(exec_cmd, stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT,shell=True)
    ret = p.wait()
    if 0 != ret:
        for line in p.stdout.readlines():
            print line
    else:
        for line in p.stdout.readlines():
            disk_info = line.split(' ')
            unmount_disks.append(disk_info[0])

    return unmount_disks

def is_exsit_part(disk):
    ret_exsit = False
    exec_cmd = ["fdisk -l /dev/" + disk + " | awk '/^\\/dev\\//{print $0}'"]

    p = proc.Popen(exec_cmd, stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT,shell=True)
    ret = p.wait()
    if 0 != ret:
        ret_exsit = True
        for line in p.stdout.readlines():
            print line
    else:
        for line in p.stdout.readlines():
            if line != "":
                ret_exsit = True

    return ret_exsit

#config:
def config_scan_disk():
    # Todo
    return None


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help='"auto" or "config" mode...', nargs=1)
    args = parser.parse_args()

    mode = args.mode[0]

    if mode == 'auto':
        ret = auto_scan_disk()
    elif mode == 'config':
        ret = config_scan_disk()
    else:
        ret = None

    if ret == None:
        print "No Disk Found"
    else:
        print ret
