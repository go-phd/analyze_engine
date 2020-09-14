#!/bin/bash
# author:chenyan

basedir=`cd $(dirname $0); pwd -P`
install_dir=/usr/local/venus

rm bin/ -rf
mkdir bin
cd cpp
rm build/ -rf; mkdir build; cd build
cmake ..
make; make install
cp ../libs/third_lib/lib/*/lib* $install_dir/lib64 -df
cp $install_dir/bin/* $basedir/bin/

