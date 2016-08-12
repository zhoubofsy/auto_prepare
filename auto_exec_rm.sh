#!/bin/sh

mkfs_exec=$1
mkfs_type=$2
mkfs_dev=$3

if [ -f "$mkfs_exec" ]; then
    python $mkfs_exec -f $mkfs_type -d $mkfs_dev
    rm -rf $mkfs_exec
fi
