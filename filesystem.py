#!/usr/bin/python
#coding:utf-8

import subprocess as sproc
import argparse
import pdb
import re

# format:
def mkfs(fs,dev):
    #pdb.set_trace()
    if fs=="" or dev == "":
        return -1

    cmd = []    
    cmd.append("mkfs")
    cmd.append("-t")
    cmd.append(fs)
    cmd.append(dev)

    p = sproc.Popen(cmd, stdin=sproc.PIPE, stdout=sproc.PIPE, stderr=sproc.STDOUT, shell=False)
    p.stdin.write("y\n")
    ret = p.wait()
    if 0 != ret:
        for line in p.stdout.readlines():
            print line
    return ret

# Is mount:
def is_mnt(path):
    #pdb.set_trace()
    ret_mnt = False
    if path == "":
        return False
    
    cmd = ["lsblk -l --output MOUNTPOINT"]
    p = sproc.Popen(cmd,stdin=sproc.PIPE,stdout=sproc.PIPE,stderr=sproc.STDOUT,shell=True)
    if 0 != p.wait():
        for line in p.stdout.readlines():
            print line
    else:
        for line in p.stdout.readlines():
            if path == line.strip():
                ret_mnt = True
    return ret_mnt

# set /etc/fstab
def set_fstab(fs,dev,mpoint):
    #pdb.set_trace()
    if fs=="" or dev=="" or mpoint=="":
        return -1
    file_name = '/etc/fstab'
    #file_name_new = file_name + '.new'
    fstab = []
    content = []
    line_bak = ""
    add_line = dev + '      ' + mpoint + '      ' + fs + '  default 0 0\n'
    # read & parse fstab
    f = open(file_name,'r+')
    if f == None:
        return -1
    f.seek(0,0)
    # read file:
    for line in f.readlines():
        content.append(line)
    # parse fstab & compare devices name
    for line in content:
        str_line = line.strip()
        if str_line == "" or str_line[0] == "#" or str_line == "\n":
            continue
        items = re.split("\s+",str_line)
        # find same devs and record line
        if items[0] == dev:
            line_bak = line
            break
    # remove same device record
    if line_bak != "":
        content.remove(line_bak)
        # rewrite fstab
        f.seek(0,0)
        f.writelines(content)
    # add new line
    f.write(add_line)
    f.close()
    return 0

# mount:
def mnt(fs,dev,mpoint):
    #pdb.set_trace()
    if fs=="" or dev=="" or mpoint=="":
        return -1

    cmd = []
    cmd.append("mount")
    cmd.append("-t")
    cmd.append(fs)
    cmd.append(dev)
    cmd.append(mpoint)

    p = sproc.Popen(cmd, stdin=sproc.PIPE, stdout=sproc.PIPE, stderr=sproc.STDOUT, shell=False)
    ret = p.wait()
    if 0 != ret:
        for line in p.stdout.readlines():
            print line
    return ret

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fs", help="Input filesystem type", nargs=1)
    parser.add_argument("-d", "--device", help="Format device", nargs=1)
    parser.add_argument("-m", "--mount", help="Mount point", nargs=1)
    args = parser.parse_args()

    #print "fs:%s,dev:%s"%(args.fs[0],args.device[0])
    
    input_fs = args.fs[0]
    input_dev = args.device[0]
    input_mount_point = args.mount[0]
    ret = 1

    if 0 == mkfs(input_fs, input_dev):
        if 0 == mnt(input_fs, input_dev, inoput_mount_point):
            ret = 0
    exit(ret)
