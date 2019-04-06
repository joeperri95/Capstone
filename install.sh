#!/bin/bash

if [ $(dpkg-query -W -f='${Status}' python3.5 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt install python3.5-dev;
fi

if [ $(dpkg-query -W -f='${Status}' python3-pip 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt install python3-pip;
fi

$(pip3 install numpy opencv-python flask gpiozero)
