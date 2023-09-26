#!/bin/bash    
CUR_PWD=$(pwd)
NICAD_INSTALL_LOCATION="/usr/local/lib/nicad6/"
cd $NICAD_INSTALL_LOCATION
yes | ./cleanall $CUR_PWD
