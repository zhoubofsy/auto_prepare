#!/usr/bin/python
#coding:utf8

import pdb
import argparse
from scan_disk import auto_scan_disk
from filesystem import mkfs
from filesystem import mnt
from filesystem import is_mnt
from filesystem import set_fstab
from service import cmd_exec
from service import cmd_exec2
from service import service_start
from service import service_del
from service import service_add

def_mnt_point = '/store'
def_fs_type = 'ext4'
def_mysql_data_src = '/cs/mysql/data'

# startup:
def startup(device, mt_point = def_mnt_point, fs_type = def_fs_type, mysql_data_src = def_mysql_data_src):
    #pdb.set_trace()
    ret = -1
    mounted = False
    fs = fs_type
    mount_point = mt_point
    data_src = mysql_data_src
    dev = device

    # 1. Scan disks
    disk = auto_scan_disk()
    if disk != None and len(disk) >= 1:
        dev = "/dev/"+disk[0]

    # 2. Format disk & mount
    if dev != "":
        if (not is_mnt(mount_point)): 
            cmd_exec("mkdir -p " + mount_point, False)
            if 0 == mkfs(fs,dev) and 0 == mnt(fs,dev,mount_point):
                # 3. Modify fstab
                set_fstab(fs,dev,mount_point)
                # 4. copy data_src to mount_point
                cmd_exec2("/bin/cp -r " + data_src + "/* " + mount_point + "/", True)
                # 5. rm -rvf /${mount_point}/lost+found
                cmd_exec2("/bin/rm -rvf "+ mount_point + "/lost+found", True)
                # 5. Remove rdsd service
                # 6. Add mysqld service
                #if 0 == service_del('rdsd') and 0 == service_add('mysqld'):
                if 0 == service_add('mysqld'):
                    # 7. Start mysqld service
                    ret = service_start('mysqld')
        else:
            ret = 0
    
    return ret
#main:
if __name__=="__main__":
    pdb.set_trace()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fs", help="", nargs='?', type=str, default=def_fs_type)
    parser.add_argument("device", help="", nargs=1, type=str)
    parser.add_argument("-m", "--mount", help="", nargs='?', type=str, default=def_mnt_point)
    parser.add_argument("-s", "--src", help="", nargs='?', type=str, default=def_mysql_data_src)
    args = parser.parse_args()

    input_fs = def_fs_type
    input_dev = ""
    input_mnt = def_mnt_point
    input_src = def_mysql_data_src

    if args.fs != None and len(args.fs) > 0:
        input_fs = args.fs
    if len(args.device) > 0:
        input_dev = args.device[0]
    if args.mount != None and len(args.mount) > 0:
        input_mnt = args.mount.rstrip('/')
    if args.src != None and len(args.src) > 0:
        input_src = args.src.rstrip('/')

    ret = startup(input_dev, input_mnt, input_fs, input_src)

    if ret == 0:
        exit(0)
    else:
        exit(1)
