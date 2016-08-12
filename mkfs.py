#coding:utf-8

import subprocess as sproc
import argparse
import pdb

def mkfs(fs,dev):
    #pdb.set_trace()
    if fs=="" or dev == "":
        return 0

    cmd = []    
    cmd.append("mkfs")
    cmd.append("-t")
    cmd.append(fs)
    cmd.append(dev)

    p = sproc.Popen(cmd, stdin=sproc.PIPE, stdout=sproc.PIPE, stderr=sproc.STDOUT, shell=False)
    p.stdin.write("y\n")
    if 0 != p.wait():
        for line in p.stdout.readlines():
            print line
    return 0

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fs", help="Input filesystem type", nargs=1)
    parser.add_argument("-d", "--device", help="Format device", nargs=1)
    args = parser.parse_args()

    print "fs:%s,dev:%s"%(args.fs[0],args.device[0])
    
    mkfs(args.fs[0], args.device[0])
