#!/bin/bash

sudo apt-get install cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev pkg-config libpcap-dev python-numpy python-qt4 

sudo pip install pyside

wget https://github.com/greatscottgadgets/libbtbb/archive/2018-12-R1.tar.gz -O libbtbb-2018-12-R1.tar.gz 

tar -xf libbtbb-2018-12-R1.tar.gz 

cd libbtbb-2018-12-R1 

mkdir build 

cd build 

cmake .. 

make 

sudo make install 

sudo ldconfig 

cd ../..

wget https://github.com/greatscottgadgets/ubertooth/releases/download/2018-12-R1/ubertooth-2018-12-R1.tar.xz 

tar xf ubertooth-2018-12-R1.tar.xz 

cd ubertooth-2018-12-R1/host 

mkdir build 

cd build 

cmake .. 

make 

sudo make install 

sudo ldconfig 

cd ../..

sudo apt-get install wireshark wireshark-dev libwireshark-dev cmake 

cd libbtbb-2018-12-R1/wireshark/plugins/btbb 

mkdir build 

cd build 

cmake -DCMAKE_INSTALL_LIBDIR=/usr/lib/x86_64-linux-gnu/wireshark/libwireshark3/plugins .. 

make 

sudo make install 

cd ../..

sudo apt-get install wireshark wireshark-dev libwireshark-dev cmake 

cd libbtbb-2018-12-R1/wireshark/plugins/btbredr 

mkdir build 

cd build 

cmake -DCMAKE_INSTALL_LIBDIR=/usr/lib/x86_64-linux-gnu/wireshark/libwireshark3/plugins .. 

make 

sudo make install 

cd ../..
