#!/usr/bin/python
#coding:utf8

import pdb
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

# startup:
def startup():
    #pdb.set_trace()
    ret = -1
    mounted = False
    fs = 'ext4'
    mount_point = '/store'
    data_src = '/cs/mysql/data'
    dev = ""

    # 1. Scan disks
    disk = auto_scan_disk()
    if disk != None and len(disk) >= 1:
        dev = disk[0]

    # 2. Format disk & mount
    if dev != "":
        if (not is_mnt(mount_point)): 
            cmd_exec("mkdir -p " + mount_point, False)
            if 0 == mkfs(fs,"/dev/"+dev) and 0 == mnt(fs,"/dev/"+dev,mount_point):
                # 3. Modify fstab
                set_fstab(fs,"/dev/"+dev,mount_point)
                # 4. copy data_src to mount_point
                cmd_exec2("/bin/cp -r " + data_src + "/* " + mount_point + "/", True)
                # 5. Remove rdsd service
                # 6. Add mysqld service
                if 0 == service_del('rdsd') and 0 == service_add('mysqld'):
                    # 7. Start mysqld service
                    ret = service_start('mysqld')
        else:
            ret = 0
    
    return ret
#main:
if __name__=="__main__":

    ret = startup()

    if ret == 0:
        exit(0)
    else:
        exit(1)
