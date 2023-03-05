#!/bin/bash

sudo echo ""

echo "download & install cvc5"
sudo sh ./install_cvc5.sh
echo "cvc5 finished"

echo "download & install iprover"
sudo sh ./install_iprover.sh
echo "iprover finished"

echo "download & install leo3"
sudo sh ./install_leo3.sh
echo "leo3 finished"

echo "download & install princess"
sudo sh ./install_princess.sh
echo "princess finished"

echo "download & install vampire"
sudo sh ./install_vampire.sh
echo "vampire finished"

