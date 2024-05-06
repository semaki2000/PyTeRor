#!/bin/bash    
CUR_PWD=$(pwd)
NICAD_INSTALL_LOCATION="/usr/local/lib/nicad6/" #nicad install location 
cd $NICAD_INSTALL_LOCATION
yes 2>/dev/null | ./cleanall $CUR_PWD #call script to clean up nicad files
