#!/bin/sh


echo "Installing GOVC..."
os=`uname -s`
which govc 1>/dev/null 2>/dev/null
if [ $? -ne 0 ]; then
  if [ $os = "Linux" ]; then
        wget https://github.com/vmware/govmomi/releases/download/v0.30.4/govc_Linux_arm64.tar.gz
        gunzip govc_Linux_arm64.tar.gz
        tar -xvf govc_Linux_arm64.tar
        sudo cp -f govc /usr/local/bin/
        sudo chmod +x /usr/local/bin/govc
  elif [ $os = "Darwin" ]; then
  	print "I am here2"
        wget https://github.com/vmware/govmomi/releases/download/v0.30.4/govc_Darwin_arm64.tar.gz
        gunzip govc_Darwin_arm64.tar.gz
        tar -xvf govc_Darwin_arm64.tar
        sudo cp -f govc /usr/local/bin
        sudo chmod +x /usr/local/bin/govc
  fi
fi

echo "Installing necessary packages"

pip3 install --upgrade pip
pip3 install purestorage
pip3 install pyVim
pip3 install pyVmomi
pip3 install kubernetes

